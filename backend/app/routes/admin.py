"""Tableau de bord du super admin : gestion des comptes médecins.

Toutes les routes sont protégées par `exiger_super_admin`. Elles regroupent les
actes qui doivent rester hors de portée du médecin : valider, bloquer,
réinitialiser un mot de passe, consulter les comptes des autres praticiens.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import exiger_super_admin
from app.models.compte import Compte, DemandeReinitialisation
from app.models.enums import RoleCompte, StatutCompte, StatutDemandeReinit
from app.schemas.admin import (
    BlocageRequest,
    CompteAdminRead,
    DemandeReinitialisationRead,
    LienReinitialisationRead,
    MotDePasseTemporaireRequest,
    StatistiquesRead,
)
from app.services import comptes as comptes_service

router = APIRouter(prefix="/admin", tags=["admin"])

# L'administration ne gère pas les comptes d'administration : les lister serait
# sans intérêt et exposerait les comptes d'administration entre eux.
ADMIN_VISIBLE = Compte.role == RoleCompte.medecin


def _compte_read(compte: Compte) -> CompteAdminRead:
    return CompteAdminRead(
        id_compte=compte.id_compte,
        email=compte.email,
        nom=compte.nom,
        prenom=compte.prenom,
        role=compte.role.value,
        statut=compte.statut.value,
        telephone=compte.telephone,
        hopital=compte.hopital,
        id_medecin=compte.id_medecin,
        doit_changer_mdp=bool(compte.doit_changer_mdp),
        motif_blocage=compte.motif_blocage,
        verrouille_jusqu_a=compte.verrouille_jusqu_a,
        date_activation=compte.date_activation,
        date_derniere_connexion=compte.date_derniere_connexion,
        date_creation=compte.date_creation,
    )


def _exiger_demande(db: Session, id_demande: int) -> DemandeReinitialisation:
    demande = db.get(DemandeReinitialisation, id_demande)
    if demande is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Demande {id_demande} introuvable.",
        )
    return demande


# ---------------------------------------------------------------------------
# Vue d'ensemble
# ---------------------------------------------------------------------------


@router.get("/statistiques", response_model=StatistiquesRead)
def statistiques(
    db: Session = Depends(get_db),
    _: Compte = Depends(exiger_super_admin),
):
    """Compteurs affichés en tête du tableau de bord."""
    return comptes_service.statistiques(db)


@router.get("/comptes", response_model=list[CompteAdminRead])
def lister_comptes(
    statut: StatutCompte | None = Query(default=None),
    recherche: str | None = Query(default=None, max_length=120),
    db: Session = Depends(get_db),
    _: Compte = Depends(exiger_super_admin),
):
    """Comptes médecins, filtrables par statut et cherchables par identité.

    `recherche` porte sur le nom, le prénom, l'email et l'établissement : c'est
    ce que l'admin connaît d'un collègue lorsqu'un médecin l'appelle (« le Dr
    Benali de l'EHS Aïn Taya »).
    """
    query = db.query(Compte).filter(ADMIN_VISIBLE)

    if statut is not None:
        query = query.filter(Compte.statut == statut)

    if recherche:
        motif = f"%{recherche.strip()}%"
        query = query.filter(
            or_(
                Compte.nom.ilike(motif),
                Compte.prenom.ilike(motif),
                Compte.email.ilike(motif),
                Compte.hopital.ilike(motif),
            )
        )

    return [_compte_read(c) for c in query.order_by(Compte.date_creation.desc()).all()]


# ---------------------------------------------------------------------------
# Cycle de vie d'un compte
# ---------------------------------------------------------------------------


@router.post("/comptes/{id_compte}/accepter", response_model=CompteAdminRead)
def accepter_compte(
    id_compte: int,
    db: Session = Depends(get_db),
    admin: Compte = Depends(exiger_super_admin),
):
    """Valide une inscription : le compte devient actif et gagne son profil."""
    return _compte_read(comptes_service.accepter_compte(db, id_compte, admin))


@router.post("/comptes/{id_compte}/bloquer", response_model=CompteAdminRead)
def bloquer_compte(
    id_compte: int,
    payload: BlocageRequest,
    db: Session = Depends(get_db),
    admin: Compte = Depends(exiger_super_admin),
):
    """Bloque un compte. Ses sessions en cours cessent de fonctionner aussitôt."""
    return _compte_read(comptes_service.bloquer_compte(db, id_compte, admin, payload.motif))


@router.post("/comptes/{id_compte}/debloquer", response_model=CompteAdminRead)
def debloquer_compte(
    id_compte: int,
    db: Session = Depends(get_db),
    _: Compte = Depends(exiger_super_admin),
):
    """Remet un compte bloqué en service."""
    return _compte_read(comptes_service.debloquer_compte(db, id_compte))


@router.post(
    "/comptes/{id_compte}/mot-de-passe-temporaire", response_model=CompteAdminRead
)
def mot_de_passe_temporaire(
    id_compte: int,
    payload: MotDePasseTemporaireRequest,
    db: Session = Depends(get_db),
    _: Compte = Depends(exiger_super_admin),
):
    """Impose un mot de passe provisoire au médecin.

    Complément du lien à usage unique, pour les médecins qui ne peuvent pas
    l'utiliser. Le médecin devra le changer à sa prochaine connexion.
    """
    compte = comptes_service.definir_mot_de_passe_temporaire(
        db, id_compte, payload.nouveau_mot_de_passe
    )
    return _compte_read(compte)


# ---------------------------------------------------------------------------
# Demandes de réinitialisation
# ---------------------------------------------------------------------------


@router.get("/demandes-reinitialisation", response_model=list[DemandeReinitialisationRead])
def lister_demandes(
    statut: StatutDemandeReinit = Query(default=StatutDemandeReinit.en_attente),
    db: Session = Depends(get_db),
    _: Compte = Depends(exiger_super_admin),
):
    """File des demandes de mot de passe oublié, la plus ancienne d'abord.

    L'ordre d'arrivée est l'ordre de traitement, et une demande ancienne est
    par définition celle qui attend depuis le plus longtemps.
    """
    demandes = (
        db.query(DemandeReinitialisation)
        .join(Compte, Compte.id_compte == DemandeReinitialisation.id_compte)
        .filter(DemandeReinitialisation.statut == statut)
        .order_by(DemandeReinitialisation.date_demande.asc())
        .all()
    )
    return [
        DemandeReinitialisationRead(
            id_demande=demande.id_demande,
            id_compte=demande.id_compte,
            email=demande.compte.email,
            nom=demande.compte.nom,
            prenom=demande.compte.prenom,
            hopital=demande.compte.hopital,
            statut=demande.statut.value,
            motif=demande.motif,
            expire_le=demande.expire_le,
            date_demande=demande.date_demande,
            date_traitement=demande.date_traitement,
        )
        for demande in demandes
    ]


@router.post(
    "/demandes-reinitialisation/{id_demande}/lien",
    response_model=LienReinitialisationRead,
)
def generer_lien(
    id_demande: int,
    db: Session = Depends(get_db),
    admin: Compte = Depends(exiger_super_admin),
):
    """Émet le lien de réinitialisation d'une demande.

    Le lien n'est renvoyé qu'ici, une seule fois : la base n'en conserve que
    l'empreinte. L'admin doit donc le transmettre au médecin avant de quitter
    la page ; s'il le perd, il en régénère un.
    """
    demande = _exiger_demande(db, id_demande)
    lien, demande = comptes_service.generer_lien_reinitialisation(
        db, demande.id_compte, admin
    )
    return LienReinitialisationRead(
        id_demande=demande.id_demande,
        lien=lien,
        expire_le=demande.expire_le,
        message=(
            "Transmettez ce lien au médecin par un canal sûr (appel "
            "téléphonique ou messagerie). Il est valable "
            f"{settings.DUREE_JETON_REINIT_MINUTES} minutes et ne fonctionne "
            "qu'une seule fois."
        ),
    )


@router.post("/demandes-reinitialisation/{id_demande}/cloturer")
def cloturer_demande(
    id_demande: int,
    statut: StatutDemandeReinit = Query(default=StatutDemandeReinit.traitee),
    db: Session = Depends(get_db),
    admin: Compte = Depends(exiger_super_admin),
):
    """Clôt une demande.

    `traitee` quand le médecin a récupéré son accès, `annulee` quand elle est
    devenue sans objet (compte bloqué entre-temps, erreur de saisie).
    """
    if statut is StatutDemandeReinit.en_attente:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Une demande se clôture comme « traitée » ou « annulée ».",
        )
    return comptes_service.cloturer_demande(db, id_demande, admin, statut).id_demande