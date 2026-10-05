"""Authentification publique : inscription, connexion, mot de passe oublié.

La validation des comptes, leur blocage et la génération des liens de
réinitialisation sont des actes d'administration : ils vivent dans
`app/routes/admin.py`, protégés par `exiger_super_admin`. Un médecin ne peut
donc ni s'auto-valider, ni se déverrouiller, ni obtenir un lien de
réinitialisation sans passer par l'administration.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_compte_actif, get_medecin_for_user
from app.models.compte import Compte
from app.models.medecin import Medecin
from app.schemas.auth import PASSWORD_POLICY, PasswordPolicy
from app.services import comptes as comptes_service

router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger(__name__)

# Tailles des colonnes `medecin` / `compte` (cf. database/*.sql). Sans ce
# contrôle, un champ trop long provoque une StringDataRightTruncation côté
# Postgres, remontée en 500 « impossible d'enregistrer le profil » : un
# message incompréhensible pour une simple saisie trop longue.
CHAMPS_LIMITES: dict[str, tuple[int, str]] = {
    "nom": (100, "Nom"),
    "prenom": (100, "Prénom"),
    "email": (255, "Adresse email"),
    "telephone": (30, "Numéro de téléphone"),
    "hopital": (150, "Établissement / Hôpital"),
}


class SignupRequest(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    telephone: str | None = None
    hopital: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    jeton: str = Field(min_length=1)
    nouveau_mot_de_passe: str


class ChangePasswordRequest(BaseModel):
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str


class CompteRead(BaseModel):
    """Compte tel que le frontend le connaît : c'est lui qui décide vers quel
    espace rediriger après connexion."""

    id_compte: int
    email: str
    nom: str
    prenom: str
    role: str
    statut: str
    hopital: str | None = None
    doit_changer_mdp: bool


class MedecinRead(BaseModel):
    id_medecin: int
    nom: str
    prenom: str
    email: str
    telephone: str | None = None
    hopital: str | None = None


class SessionRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
    compte: CompteRead
    doit_changer_mdp: bool


def _verifier_longueurs(payload) -> None:
    depassements = [
        f"{libelle} : maximum {maximum} caractères"
        for champ, (maximum, libelle) in CHAMPS_LIMITES.items()
        if len(getattr(payload, champ) or "") > maximum
    ]
    if depassements:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=" ; ".join(depassements),
        )


def _compte_read(compte: Compte) -> CompteRead:
    return CompteRead(
        id_compte=compte.id_compte,
        email=compte.email,
        nom=compte.nom,
        prenom=compte.prenom,
        role=compte.role.value,
        statut=compte.statut.value,
        hopital=compte.hopital,
        doit_changer_mdp=bool(compte.doit_changer_mdp),
    )


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------


@router.post("/signup", status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    """Inscrit un médecin. Le compte reste **en attente** jusqu'à validation.

    Aucun jeton n'est renvoyé, volontairement : tant que le super admin n'a pas
    accepté, le médecin n'a rien à ouvrir. La réponse lui dit quoi attendre.
    """
    _verifier_longueurs(payload)
    compte = comptes_service.inscrire_medecin(db, payload)

    return {
        "compte": _compte_read(compte).model_dump(),
        "message": (
            "Votre demande d'inscription a été transmise à l'administration. "
            "Votre compte sera actif dès sa validation ; vous pourrez alors "
            "vous connecter avec cette adresse email."
        ),
    }


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------


@router.post("/login", response_model=SessionRead)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authentifie un compte actif et renvoie son jeton de session.

    Un compte en attente reçoit 403 avec la raison : le médecin doit savoir
    que son inscription est simplement en cours de traitement, et non qu'il a
    mal saisi ses identifiants.
    """
    compte, jeton = comptes_service.connecter(db, payload.email, payload.password)
    return SessionRead(
        access_token=jeton,
        compte=_compte_read(compte),
        doit_changer_mdp=bool(compte.doit_changer_mdp),
    )


@router.get("/me")
def current_session(
    compte: Compte = Depends(get_compte_actif),
    db: Session = Depends(get_db),
):
    """Compte et profil clinique du connecté.

    Le frontend s'en sert pour router vers l'espace admin ou l'espace médecin,
    et pour afficher l'identité réelle plutôt qu'un nom codé en dur.
    """
    medecin = db.get(Medecin, compte.id_medecin) if compte.id_medecin is not None else None
    return {
        "compte": _compte_read(compte).model_dump(),
        "medecin": (
            MedecinRead(
                id_medecin=medecin.id_medecin,
                nom=medecin.nom,
                prenom=medecin.prenom,
                email=medecin.email,
                telephone=medecin.telephone,
                hopital=medecin.hopital,
            ).model_dump()
            if medecin is not None
            else None
        ),
    }


@router.get("/me/medecin", response_model=MedecinRead)
def current_medecin(medecin: Medecin = Depends(get_medecin_for_user)):
    """Profil clinique seul, pour les écrans qui n'ont pas besoin du rôle."""
    return MedecinRead(
        id_medecin=medecin.id_medecin,
        nom=medecin.nom,
        prenom=medecin.prenom,
        email=medecin.email,
        telephone=medecin.telephone,
        hopital=medecin.hopital,
    )


@router.get("/password-policy", response_model=PasswordPolicy)
def password_policy():
    """Règles de mot de passe en vigueur.

    Route publique : elle est consommée par les formulaires pour afficher au
    médecin ce qu'il lui reste à satisfaire, avant même l'envoi.
    """
    return PASSWORD_POLICY


# ---------------------------------------------------------------------------
# Mot de passe
# ---------------------------------------------------------------------------


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Enregistre une demande de réinitialisation pour l'administration.

    La plateforme n'envoie aucun email : la demande apparaît dans le tableau
    de bord du super admin, qui génère le lien et le transmet au médecin.

    Le message est rigoureusement identique que l'adresse existe ou non, sinon
    la page deviendrait un oracle d'énumération : on testerait des adresses et
    on saurait lesquelles sont inscrites. Le service applique déjà cette règle
    en ne divulguant rien ; ce n'est pas à la route de la contredire.
    """
    comptes_service.demander_reinitialisation(db, payload.email)

    return {
        "message": (
            "Votre demande a été transmise à l'administration. "
            "Un administrateur vous communiquera un lien de réinitialisation, "
            "valable une heure et utilisable une seule fois."
        ),
        # Le frontend affiche le délai réel sans avoir à le réinventer.
        "delai_validite_minutes": settings.DUREE_JETON_REINIT_MINUTES,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Nouveau mot de passe à partir du jeton remis par l'administration."""
    comptes_service.reinitialiser_mot_de_passe(
        db, payload.jeton, payload.nouveau_mot_de_passe
    )
    return {"message": "Mot de passe mis à jour. Vous pouvez vous connecter."}


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    compte: Compte = Depends(get_compte_actif),
    db: Session = Depends(get_db),
):
    """Change le mot de passe du compte connecté.

    Route de sortie pour un mot de passe posé par l'administration : sans elle,
    un médecin réinitialisé par l'admin devrait le solliciter à nouveau pour
    tout changement de mot de passe.
    """
    comptes_service.changer_mot_de_passe(
        db, compte, payload.ancien_mot_de_passe, payload.nouveau_mot_de_passe
    )
    return {"message": "Mot de passe mis à jour."}