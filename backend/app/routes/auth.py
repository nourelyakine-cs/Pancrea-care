from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.supabase import get_current_user, supabase

router = APIRouter(prefix="/auth", tags=["auth"])


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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed (email already registered?)",
        )

    medecin = Medecin(
        nom=payload.nom,
        prenom=payload.prenom,
        email=payload.email,
        telephone=payload.telephone,
        hopital=payload.hopital,
    )
    db.add(medecin)
    db.commit()

    return {
        "user": res.user.id,
        "medecin_id": medecin.id_medecin,
        "need_email_confirmation": res.session is None,
    }


@router.post("/login")
def login(payload: LoginRequest):
    res = supabase.auth.sign_in_with_password(
        {"email": payload.email, "password": payload.password}
    )
    return {
        "access_token": res.session.access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    medecin = db.query(Medecin).filter(Medecin.email == user.email).first()
    return {
        "id": user.id,
        "email": user.email,
        "medecin": {
            "id_medecin": medecin.id_medecin,
            "nom": medecin.nom,
            "prenom": medecin.prenom,
            "telephone": medecin.telephone,
            "hopital": medecin.hopital,
        } if medecin else None,
    }