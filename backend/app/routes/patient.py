from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.full_patient import FullPatientCreate, FullPatientRead
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services import full_patient as full_patient_service
from app.services import patient as patient_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/full", response_model=FullPatientRead, status_code=201)
def create_patient_full(
    payload: FullPatientCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    """Crée en une seule requête : patient + dossier + première évaluation
    (toutes les données) + décision. Répond à la fiche unique de saisie."""
    return full_patient_service.create_full_patient(db, payload, medecin.id_medecin)


@router.post("/", response_model=PatientRead, status_code=201)
def create_patient(
    payload: PatientCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return patient_service.create_patient(db, payload, medecin.id_medecin)


@router.get("/", response_model=list[PatientRead])
def list_patients(
    nom: str | None = None,
    sexe: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return patient_service.list_patients(db, nom, sexe, skip, limit)


@router.get("/{id_patient}", response_model=PatientRead)
def get_patient(
    id_patient: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return patient_service.get_patient(db, id_patient)


@router.put("/{id_patient}", response_model=PatientRead)
def update_patient(
    id_patient: int,
    payload: PatientUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return patient_service.update_patient(db, id_patient, payload, medecin.id_medecin)


@router.delete("/{id_patient}", status_code=204)
def delete_patient(
    id_patient: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    patient_service.delete_patient(db, id_patient, medecin.id_medecin)
