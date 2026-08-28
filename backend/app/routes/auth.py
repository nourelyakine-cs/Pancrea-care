from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.auth import (
    ForgotPasswordRequest,
    MedecinLogin,
    MedecinRegister,
    MedecinResponse,
    ResetPasswordRequest,
    TokenResponse,
)
from app.services.auth import create_password_reset_token, login, register, reset_password
from app.services.email import resend_configured, send_password_reset_email
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MedecinResponse, status_code=status.HTTP_201_CREATED)
def register_medecin(medecin_data: MedecinRegister, db: Session = Depends(get_db)):
    try:
        medecin = register(db, medecin_data)
        return medecin
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    message = "If this email is registered, a reset link has been sent"

    medecin = db.query(Medecin).filter(Medecin.email == data.email).first()
    if not medecin:
        return {"message": message}

    if not resend_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service is not configured on the server",
        )

    try:
        token = create_password_reset_token(medecin.email)
        send_password_reset_email(medecin.email, token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send the reset email",
        )

    return {"message": message}


@router.post("/reset-password")
def reset_password_medecin(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_password(db, data.token, data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Password has been reset"}


@router.post("/login", response_model=TokenResponse)
def login_medecin(medecin_data: MedecinLogin, db: Session = Depends(get_db)):
    try:
        tokens = login(db, medecin_data.email, medecin_data.password)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=MedecinResponse)
def get_me(current_user: Medecin = Depends(get_current_user)):
    return current_user
