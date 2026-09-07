from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.audit import AuditRead
from app.services import audit as audit_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/", response_model=list[AuditRead])
def list_audit(
    id_medecin: int | None = None,
    type_entite: str | None = None,
    id_entite: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return audit_service.list_audit(db, id_medecin, type_entite, id_entite, skip, limit)
