from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.dossier import (
    AntecedentCreate,
    AntecedentRead,
    AntecedentUpdate,
    DossierCreate,
    DossierRead,
    DossierUpdate,
    MutationCreate,
    MutationRead,
    MutationUpdate,
)
from app.schemas.dossier_detail import DossierDetailRead
from app.services import dossier as dossier_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/dossiers", tags=["dossiers"])


@router.post("/patients/{id_patient}", response_model=DossierRead, status_code=201)
def create_dossier(
    id_patient: int,
    payload: DossierCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.create_dossier(db, id_patient, payload, medecin.id_medecin)


@router.get("/", response_model=list[DossierRead])
def list_dossiers(
    statut: str | None = None,
    id_patient: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.list_dossiers(db, statut, id_patient, skip, limit)


@router.get("/full/{id_dossier}", response_model=DossierDetailRead)
def get_dossier_full(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.get_dossier_detail(db, id_dossier)


@router.get("/{id_dossier}", response_model=DossierRead)
def get_dossier(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.get_dossier(db, id_dossier)


@router.put("/{id_dossier}", response_model=DossierRead)
def update_dossier(
    id_dossier: int,
    payload: DossierUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.update_dossier(db, id_dossier, payload, medecin.id_medecin)


@router.post("/{id_dossier}/close", response_model=DossierRead)
def close_dossier(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.set_dossier_statut(db, id_dossier, "clos", medecin.id_medecin)


@router.post("/{id_dossier}/archive", response_model=DossierRead)
def archive_dossier(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.set_dossier_statut(db, id_dossier, "archive", medecin.id_medecin)


# --- Antécédents familiaux --------------------------------------------------


@router.get("/{id_dossier}/antecedents", response_model=list[AntecedentRead])
def list_antecedents(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.list_antecedents(db, id_dossier)


@router.post("/{id_dossier}/antecedents", response_model=AntecedentRead, status_code=201)
def create_antecedent(
    id_dossier: int,
    payload: AntecedentCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.create_antecedent(db, id_dossier, payload, medecin.id_medecin)


@router.put("/antecedents/{id_antecedent}", response_model=AntecedentRead)
def update_antecedent(
    id_antecedent: int,
    payload: AntecedentUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.update_antecedent(db, id_antecedent, payload, medecin.id_medecin)


@router.delete("/antecedents/{id_antecedent}", status_code=204)
def delete_antecedent(
    id_antecedent: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    dossier_service.delete_antecedent(db, id_antecedent, medecin.id_medecin)


# --- Mutations germinales ---------------------------------------------------


@router.get("/{id_dossier}/mutations", response_model=list[MutationRead])
def list_mutations(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.list_mutations(db, id_dossier)


@router.post("/{id_dossier}/mutations", response_model=MutationRead, status_code=201)
def create_mutation(
    id_dossier: int,
    payload: MutationCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.create_mutation(db, id_dossier, payload, medecin.id_medecin)


@router.put("/mutations/{id_mutation}", response_model=MutationRead)
def update_mutation(
    id_mutation: int,
    payload: MutationUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return dossier_service.update_mutation(db, id_mutation, payload, medecin.id_medecin)


@router.delete("/mutations/{id_mutation}", status_code=204)
def delete_mutation(
    id_mutation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    dossier_service.delete_mutation(db, id_mutation, medecin.id_medecin)
