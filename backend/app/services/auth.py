from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.medecin import Medecin
from app.schemas.auth import MedecinRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def register(db: Session, medecin_data: MedecinRegister) -> Medecin:
    existing = db.query(Medecin).filter(Medecin.email == medecin_data.email).first()
    if existing:
        raise ValueError("Email already registered")

    medecin = Medecin(
        nom=medecin_data.nom,
        prenom=medecin_data.prenom,
        email=medecin_data.email,
        mot_de_passe_hash=hash_password(medecin_data.password),
        telephone=medecin_data.telephone,
        specialite=medecin_data.specialite,
    )
    db.add(medecin)
    db.commit()
    db.refresh(medecin)
    return medecin


def login(db: Session, email: str, password: str) -> dict:
    medecin = db.query(Medecin).filter(Medecin.email == email).first()
    if not medecin or not verify_password(password, medecin.mot_de_passe_hash):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(data={"sub": str(medecin.id_medecin)})
    refresh_token = create_refresh_token(data={"sub": str(medecin.id_medecin)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
