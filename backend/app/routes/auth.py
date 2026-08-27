from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.auth import MedecinLogin, MedecinRegister, MedecinResponse, TokenResponse
from app.services.auth import login, register
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MedecinResponse, status_code=status.HTTP_201_CREATED)
def register_medecin(medecin_data: MedecinRegister, db: Session = Depends(get_db)):
    try:
        medecin = register(db, medecin_data)
        return medecin
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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
