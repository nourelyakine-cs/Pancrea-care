from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.dossier_detail import DossierDetailRead
from app.services import dossier as dossier_service
from app.dependencies import get_medecin_for_user

router = APIRouter(prefix="/dossiers", tags=["dossiers"])


@router.get("/full/{id_dossier}", response_model=DossierDetailRead)
def get_dossier_full(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    """Dossier consolidé : identité du patient et évaluations avec biologie,
    histologie et imagerie. Alimente le pré-remplissage de l'écran d'édition."""
    return dossier_service.get_dossier_detail(db, id_dossier, medecin.id_medecin)
