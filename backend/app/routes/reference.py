from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.reference import (
    ComorbiditeCreate,
    ComorbiditeRead,
    ComorbiditeUpdate,
    GeneCreate,
    GeneRead,
    GeneUpdate,
    ProtocoleContexteCreate,
    ProtocoleContexteRead,
    ProtocoleCreate,
    ProtocoleRead,
    ProtocoleUpdate,
    SourceCreate,
    SourceRead,
    SourceUpdate,
)
from app.services import reference as reference_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/referentials", tags=["referentials"])


# --- Gene ---------------------------------------------------------------------


@router.get("/genes", response_model=list[GeneRead])
def list_genes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.list_genes(db, skip, limit)


@router.post("/genes", response_model=GeneRead, status_code=201)
def create_gene(
    payload: GeneCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.create_gene(db, payload, medecin.id_medecin)


@router.get("/genes/{id_gene}", response_model=GeneRead)
def get_gene(
    id_gene: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.get_gene(db, id_gene)


@router.put("/genes/{id_gene}", response_model=GeneRead)
def update_gene(
    id_gene: int,
    payload: GeneUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.update_gene(db, id_gene, payload, medecin.id_medecin)


# --- Comorbidité ----------------------------------------------------------------


@router.get("/comorbidites", response_model=list[ComorbiditeRead])
def list_comorbidites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.list_comorbidites(db, skip, limit)


@router.post("/comorbidites", response_model=ComorbiditeRead, status_code=201)
def create_comorbidite(
    payload: ComorbiditeCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.create_comorbidite(db, payload, medecin.id_medecin)


@router.get("/comorbidites/{id_comorbidite}", response_model=ComorbiditeRead)
def get_comorbidite(
    id_comorbidite: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.get_comorbidite(db, id_comorbidite)


@router.put("/comorbidites/{id_comorbidite}", response_model=ComorbiditeRead)
def update_comorbidite(
    id_comorbidite: int,
    payload: ComorbiditeUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.update_comorbidite(db, id_comorbidite, payload, medecin.id_medecin)


# --- Protocole ------------------------------------------------------------------


@router.get("/protocoles", response_model=list[ProtocoleRead])
def list_protocoles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.list_protocoles(db, skip, limit)


@router.post("/protocoles", response_model=ProtocoleRead, status_code=201)
def create_protocole(
    payload: ProtocoleCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.create_protocole(db, payload, medecin.id_medecin)


@router.get("/protocoles/{id_protocole}", response_model=ProtocoleRead)
def get_protocole(
    id_protocole: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.get_protocole(db, id_protocole)


@router.put("/protocoles/{id_protocole}", response_model=ProtocoleRead)
def update_protocole(
    id_protocole: int,
    payload: ProtocoleUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.update_protocole(db, id_protocole, payload, medecin.id_medecin)


@router.get("/protocoles/{id_protocole}/contextes", response_model=list[ProtocoleContexteRead])
def list_protocole_contextes(
    id_protocole: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.list_protocole_contextes(db, id_protocole)


@router.post("/protocoles/{id_protocole}/contextes", response_model=ProtocoleContexteRead, status_code=201)
def add_protocole_contexte(
    id_protocole: int,
    payload: ProtocoleContexteCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.add_protocole_contexte(db, id_protocole, payload, medecin.id_medecin)


@router.delete("/protocoles/{id_protocole}/contextes/{contexte_usage}", status_code=204)
def remove_protocole_contexte(
    id_protocole: int,
    contexte_usage: str,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    reference_service.remove_protocole_contexte(db, id_protocole, contexte_usage, medecin.id_medecin)


# --- Source référentiel --------------------------------------------------------------


@router.get("/sources", response_model=list[SourceRead])
def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.list_sources(db, skip, limit)


@router.post("/sources", response_model=SourceRead, status_code=201)
def create_source(
    payload: SourceCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.create_source(db, payload, medecin.id_medecin)


@router.get("/sources/{id_source}", response_model=SourceRead)
def get_source(
    id_source: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.get_source(db, id_source)


@router.put("/sources/{id_source}", response_model=SourceRead)
def update_source(
    id_source: int,
    payload: SourceUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return reference_service.update_source(db, id_source, payload, medecin.id_medecin)
