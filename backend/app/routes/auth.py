from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from supabase_auth.errors import AuthApiError

from app.database import get_db
from app.models.medecin import Medecin
from app.supabase import get_current_user, supabase

router = APIRouter(prefix="/auth", tags=["auth"])


def _auth_error(exc: Exception) -> HTTPException:
    """Convertit une erreur Supabase/GoTrue en HTTPException lisible.

    Sans ce mapping, une exception non capturée remonte en 500 Internal Server
    Error même pour des causes courantes (mauvais identifiants, email déjà pris,
    limite de débit email 429).
    """
    if isinstance(exc, AuthApiError):
        message = (exc.message or "").lower()
        if "rate limit" in message:
            return HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Limite de tentatives dépassée (rate limiting). "
                    "Attendez quelques minutes avant de réessayer."
                ),
            )
        if "already registered" in message or "already" in message:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Un compte existe déjà avec cet email.",
            )
        if "invalid login credentials" in message or "invalid" in message:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe invalide.",
            )
        if "email not confirmed" in message:
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email non confirmé. Vérifiez votre boîte mail.",
            )
        # erreur GoTrue identifiée mais non catégorisée
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message or "Erreur d'authentification.",
        )
    # erreur inattendue / d'infrastructure
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Le service d'authentification est momentanément indisponible.",
    )


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


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    try:
        res = supabase.auth.sign_up(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:
        raise _auth_error(exc)

    try:
        medecin = Medecin(
            nom=payload.nom,
            prenom=payload.prenom,
            email=payload.email,
            telephone=payload.telephone,
            hopital=payload.hopital,
        )
        db.add(medecin)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Compte créé mais impossible d'enregistrer le profil médecin.",
        )

    return {
        "user": res.user.id,
        "medecin_id": medecin.id_medecin,
        "need_email_confirmation": res.session is None,
    }


@router.post("/login")
def login(payload: LoginRequest):
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:
        raise _auth_error(exc)

    return {
        "access_token": res.session.access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if isinstance(user, dict):
        user_id = user["id"]
        email = user["email"]
    else:
        user_id = user.id
        email = user.email
    medecin = db.query(Medecin).filter(Medecin.email == email).first()
    return {
        "id": user_id,
        "email": email,
        "medecin": {
            "id_medecin": medecin.id_medecin,
            "nom": medecin.nom,
            "prenom": medecin.prenom,
            "telephone": medecin.telephone,
            "hopital": medecin.hopital,
        } if medecin else None,
    }