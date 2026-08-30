from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.traitement import TraitementCreate, TraitementRead, TraitementUpdate
from app.services import traitement as traitement_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/traitements", tags=["traitements"])


@router.post("/dossiers/{id_dossier}", response_model=TraitementRead, status_code=201)
def create_traitement(
    id_dossier: int,
    payload: TraitementCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return traitement_service.create_traitement(db, id_dossier, payload, medecin.id_medecin)


@router.get("/dossiers/{id_dossier}", response_model=list[TraitementRead])
def list_traitements(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return traitement_service.list_traitements(db, id_dossier)


@router.get("/{id_traitement}", response_model=TraitementRead)
def get_traitement(
    id_traitement: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return traitement_service.get_traitement(db, id_traitement)


@router.put("/{id_traitement}", response_model=TraitementRead)
def update_traitement(
    id_traitement: int,
    payload: TraitementUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return traitement_service.update_traitement(db, id_traitement, payload, medecin.id_medecin)


@router.delete("/{id_traitement}", status_code=204)
def delete_traitement(
    id_traitement: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    traitement_service.delete_traitement(db, id_traitement, medecin.id_medecin)
