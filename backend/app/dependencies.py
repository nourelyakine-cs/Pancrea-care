"""Résolution de l'identité de l'appelant et contrôle d'accès.

Remplace l'ancien `app/supabase.py` : l'identité ne vient plus d'un service
externe mais d'un jeton signé par l'API, dont le compte correspondant est relu
en base à chaque requête.

Cette relecture systématique est un choix, pas une commodité : c'est elle qui
fait qu'un blocage décidé par l'admin prend effet immédiatement sur les
sessions déjà ouvertes, sans attendre l'expiration du jeton.
"""

import logging
from datetime import datetime, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.compte import Compte
from app.models.enums import RoleCompte, StatutCompte
from app.models.medecin import Medecin
from app.services import securite

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)

# Compte utilisé quand DISABLE_AUTH court-circuite l'authentification (démo).
DEMO_MEDECIN_EMAIL = "dev@local"


def _non_authentifie(detail: str = "Authentification requise.") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _compte_demo(db: Session) -> Compte:
    """Compte éphémère utilisé en mode développement sans authentification.

    Il lui faut **aussi** un profil `medecin` : toutes les routes cliniques
    passent par `get_medecin_for_user`, qui refuse un compte sans profil. Sans
    ce rattachement, `DISABLE_AUTH=True` donnerait accès à `/admin` et à
    `/auth/me` mais renverrait 403 sur le moindre dossier patient.
    """
    compte = db.query(Compte).filter(func.lower(Compte.email) == DEMO_MEDECIN_EMAIL).first()
    if compte is None:
        medecin = (
            db.query(Medecin).filter(func.lower(Medecin.email) == DEMO_MEDECIN_EMAIL).first()
        )
        if medecin is None:
            medecin = Medecin(
                nom="Démo",
                prenom="Dev",
                email=DEMO_MEDECIN_EMAIL,
                telephone="",
                hopital="CHU (mode démo)",
            )
            db.add(medecin)
            db.flush()

        compte = Compte(
            email=DEMO_MEDECIN_EMAIL,
            # Empreinte d'un mot de passe arbitraire : ce compte n'est jamais
            # atteint par un jeton, il n'existe que pour l'affichage.
            mot_de_passe_hash=securite.hacher_mot_de_passe("demo-desactivation-auth"),
            role=RoleCompte.medecin,
            statut=StatutCompte.actif,
            nom="Démo",
            prenom="Dev",
            hopital="CHU (mode démo)",
            id_medecin=medecin.id_medecin,
            date_activation=datetime.now(timezone.utc),
        )
        db.add(compte)
        db.commit()
        db.refresh(compte)
    return compte


def get_compte_actif(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Compte:
    """Compte correspondant au jeton `Authorization: Bearer ...`.

    Renvoie 401 si le jeton est absent, expiré ou altéré, et 403 dès que le
    compte n'est plus actif — un compte validé puis bloqué perd donc l'accès
    sans qu'il ait à se reconnecter.
    """
    if settings.DISABLE_AUTH:
        return _compte_demo(db)

    if credentials is None or not credentials.credentials:
        raise _non_authentifie()

    try:
        id_compte = securite.id_compte_du_jeton(credentials.credentials)
    except jwt.InvalidTokenError:
        raise _non_authentifie("Session expirée ou invalide. Reconnectez-vous.")
    except (KeyError, ValueError, TypeError):
        raise _non_authentifie("Session invalide. Reconnectez-vous.")

    compte = db.get(Compte, id_compte)
    if compte is None:
        raise _non_authentifie("Session invalide. Reconnectez-vous.")

    if compte.statut is StatutCompte.en_attente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre compte est en attente de validation par l'administration.",
        )
    if compte.statut is StatutCompte.bloque:
        motif = f" Motif : {compte.motif_blocage}" if compte.motif_blocage else ""
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Votre compte a été bloqué par l'administration.{motif}",
        )

    return compte


def exiger_super_admin(compte: Compte = Depends(get_compte_actif)) -> Compte:
    """Garde les routes `/admin` : seul un compte d'administration y accède.

    Un médecin qui appelle ces routes directement reçoit 403 — les données
    renvoyées par le tableau de bord (comptes de tous les praticiens) ne sont
    pas les siennes.
    """
    if compte.role is not RoleCompte.super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé à l'administration de la plateforme.",
        )
    return compte


def get_medecin_for_user(
    compte: Compte = Depends(get_compte_actif),
    db: Session = Depends(get_db),
) -> Medecin:
    """Profil clinique du compte connecté.

    Le profil n'existe qu'après acceptation du compte par l'administration
    (`compte.id_medecin` est renseigné à ce moment-là). Un compte sans profil
    ne peut donc pas prétendre à des données cliniques.

    Un administrateur est aussi un praticien : `bootstrap_admin` lui crée un
    profil, et il accède donc aux routes cliniques comme tout médecin. Si la
    colonne reste vide (compte créé avant cette évolution), le message le dit
    explicitement plutôt que de laisser croire à une panne.
    """
    if compte.id_medecin is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Aucun profil clinique n'est associé à ce compte. "
                "Contactez l'administration de la plateforme."
                if compte.role is RoleCompte.medecin
                else (
                    "Ce compte d'administration n'a pas de profil clinique. "
                    "Rattachez-lui-en un pour utiliser l'espace médecin : "
                    "relancez `python -m app.bootstrap_admin` après avoir "
                    "supprimé le compte, ou-contactez l'exploitation."
                )
            ),
        )

    medecin = db.get(Medecin, compte.id_medecin)
    if medecin is None:
        logger.error(
            "Compte %s référence un profil médecin inexistant (id_medecin=%s)",
            compte.email,
            compte.id_medecin,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Aucun profil clinique associé à ce compte. "
                "Contactez l'administration de la plateforme."
            ),
        )
    return medecin