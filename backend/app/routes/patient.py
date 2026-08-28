from fastapi import APIRouter, Depends

from app.models.medecin import Medecin
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/")
def list_patients(medecin: Medecin = Depends(get_medecin_for_user)):
    return {"medecin": medecin.email, "patients": []}