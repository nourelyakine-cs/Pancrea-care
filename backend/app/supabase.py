from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from supabase import create_client

from app.config import settings
from app.database import get_db
from app.models.medecin import Medecin

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = supabase.auth.get_user(credentials.credentials).user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user


def get_medecin_for_user(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Medecin:
    medecin = db.query(Medecin).filter(Medecin.email == user.email).first()
    if medecin is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No medecin account linked to this email",
        )
    return medecin
