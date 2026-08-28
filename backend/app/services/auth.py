import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.medecin import Medecin
from app.schemas.auth import MedecinRegister

_PBKDF2_ALGORITHM = "pbkdf2_sha256"
_PBKDF2_ITERATIONS = 100_000
_PBKDF2_SALT_SIZE = 16


def hash_password(password: str) -> str:
    salt = os.urandom(_PBKDF2_SALT_SIZE).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), _PBKDF2_ITERATIONS
    ).hex()
    return f"${_PBKDF2_ALGORITHM}${_PBKDF2_ITERATIONS}${salt}${digest}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        _, algorithm, iterations, salt, expected = hashed_password.split("$")
        if algorithm != _PBKDF2_ALGORITHM:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), bytes.fromhex(salt), int(iterations)
        ).hex()
        return hmac.compare_digest(digest, expected)
    except (ValueError, TypeError):
        return False


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


def create_password_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "type": "password_reset", "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_password_reset_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except JWTError:
        return None


def reset_password(db: Session, token: str, new_password: str) -> None:
    email = verify_password_reset_token(token)
    if not email:
        raise ValueError("Invalid or expired reset token")

    medecin = db.query(Medecin).filter(Medecin.email == email).first()
    if not medecin:
        raise ValueError("Account not found")

    medecin.mot_de_passe_hash = hash_password(new_password)
    db.commit()


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
