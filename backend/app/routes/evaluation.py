from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.evaluation import (
    AnalyseCreate,
    AnalyseRead,
    AnalyseUpdate,
    BiologieCreate,
    BiologieRead,
    BiologieUpdate,
    ComorbiditeEvaluationCreate,
    ComorbiditeEvaluationRead,
    ComorbiditeEvaluationUpdate,
    EvaluationCreate,
    EvaluationRead,
    EvaluationUpdate,
    HistologieCreate,
    HistologieRead,
    HistologieUpdate,
    ImagerieCreate,
    ImagerieRead,
    ImagerieUpdate,
    MetastaseCreate,
    MetastaseRead,
    MetastaseUpdate,
)
from app.services import evaluation as evaluation_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("/dossiers/{id_dossier}", response_model=EvaluationRead, status_code=201)
def create_evaluation(
    id_dossier: int,
    payload: EvaluationCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.create_evaluation(db, id_dossier, payload, medecin.id_medecin)


@router.get("/dossiers/{id_dossier}", response_model=list[EvaluationRead])
def list_evaluations(
    id_dossier: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.list_evaluations(db, id_dossier)


@router.get("/{id_evaluation}", response_model=EvaluationRead)
def get_evaluation(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.get_evaluation(db, id_evaluation)


@router.put("/{id_evaluation}", response_model=EvaluationRead)
def update_evaluation(
    id_evaluation: int,
    payload: EvaluationUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.update_evaluation(db, id_evaluation, payload, medecin.id_medecin)


@router.delete("/{id_evaluation}", status_code=204)
def delete_evaluation(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_evaluation(db, id_evaluation, medecin.id_medecin)


# --- Biologie (1:1) -----------------------------------------------------------


@router.get("/{id_evaluation}/biologie", response_model=BiologieRead)
def get_biologie(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.get_biologie(db, id_evaluation)


@router.post("/{id_evaluation}/biologie", response_model=BiologieRead, status_code=201)
def create_biologie(
    id_evaluation: int,
    payload: BiologieCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.upsert_biologie(db, id_evaluation, payload, medecin.id_medecin)


@router.put("/{id_evaluation}/biologie", response_model=BiologieRead)
def update_biologie(
    id_evaluation: int,
    payload: BiologieUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.upsert_biologie(db, id_evaluation, payload, medecin.id_medecin)


@router.delete("/{id_evaluation}/biologie", status_code=204)
def delete_biologie(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_biologie(db, id_evaluation, medecin.id_medecin)


# --- Histologie (1:1) -----------------------------------------------------------


@router.get("/{id_evaluation}/histologie", response_model=HistologieRead)
def get_histologie(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.get_histologie(db, id_evaluation)


@router.post("/{id_evaluation}/histologie", response_model=HistologieRead, status_code=201)
def create_histologie(
    id_evaluation: int,
    payload: HistologieCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.upsert_histologie(db, id_evaluation, payload, medecin.id_medecin)


@router.put("/{id_evaluation}/histologie", response_model=HistologieRead)
def update_histologie(
    id_evaluation: int,
    payload: HistologieUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.upsert_histologie(db, id_evaluation, payload, medecin.id_medecin)


@router.delete("/{id_evaluation}/histologie", status_code=204)
def delete_histologie(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_histologie(db, id_evaluation, medecin.id_medecin)


# --- Imagerie (1:N) --------------------------------------------------------------


@router.get("/{id_evaluation}/imageries", response_model=list[ImagerieRead])
def list_imageries(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.list_imageries(db, id_evaluation)


@router.post("/{id_evaluation}/imageries", response_model=ImagerieRead, status_code=201)
def create_imagerie(
    id_evaluation: int,
    payload: ImagerieCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.create_imagerie(db, id_evaluation, payload, medecin.id_medecin)


@router.get("/imageries/{id_imagerie}", response_model=ImagerieRead)
def get_imagerie(
    id_imagerie: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.get_imagerie(db, id_imagerie)


@router.put("/imageries/{id_imagerie}", response_model=ImagerieRead)
def update_imagerie(
    id_imagerie: int,
    payload: ImagerieUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.update_imagerie(db, id_imagerie, payload, medecin.id_medecin)


@router.delete("/imageries/{id_imagerie}", status_code=204)
def delete_imagerie(
    id_imagerie: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_imagerie(db, id_imagerie, medecin.id_medecin)


# --- Métastases (children de l'imagerie) -------------------------------------------


@router.get("/imageries/{id_imagerie}/metastases", response_model=list[MetastaseRead])
def list_metastases(
    id_imagerie: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.list_metastases(db, id_imagerie)


@router.post("/imageries/{id_imagerie}/metastases", response_model=MetastaseRead, status_code=201)
def create_metastase(
    id_imagerie: int,
    payload: MetastaseCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.create_metastase(db, id_imagerie, payload, medecin.id_medecin)


@router.put("/metastases/{id_metastase}", response_model=MetastaseRead)
def update_metastase(
    id_metastase: int,
    payload: MetastaseUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.update_metastase(db, id_metastase, payload, medecin.id_medecin)


@router.delete("/metastases/{id_metastase}", status_code=204)
def delete_metastase(
    id_metastase: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_metastase(db, id_metastase, medecin.id_medecin)


# --- Analyse moléculaire (1:N) ------------------------------------------------------


@router.get("/{id_evaluation}/analyses", response_model=list[AnalyseRead])
def list_analyses(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.list_analyses(db, id_evaluation)


@router.post("/{id_evaluation}/analyses", response_model=AnalyseRead, status_code=201)
def create_analyse(
    id_evaluation: int,
    payload: AnalyseCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.create_analyse(db, id_evaluation, payload, medecin.id_medecin)


@router.get("/analyses/{id_analyse}", response_model=AnalyseRead)
def get_analyse(
    id_analyse: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.get_analyse(db, id_analyse)


@router.put("/analyses/{id_analyse}", response_model=AnalyseRead)
def update_analyse(
    id_analyse: int,
    payload: AnalyseUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.update_analyse(db, id_analyse, payload, medecin.id_medecin)


@router.delete("/analyses/{id_analyse}", status_code=204)
def delete_analyse(
    id_analyse: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.delete_analyse(db, id_analyse, medecin.id_medecin)


# --- Comorbidités (liaison N:M) ------------------------------------------------------


@router.get("/{id_evaluation}/comorbidites", response_model=list[ComorbiditeEvaluationRead])
def list_comorbidites(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.list_comorbidites(db, id_evaluation)


@router.post("/{id_evaluation}/comorbidites", response_model=ComorbiditeEvaluationRead, status_code=201)
def add_comorbidite(
    id_evaluation: int,
    payload: ComorbiditeEvaluationCreate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.add_comorbidite(db, id_evaluation, payload, medecin.id_medecin)


@router.put("/{id_evaluation}/comorbidites/{id_comorbidite}", response_model=ComorbiditeEvaluationRead)
def update_comorbidite(
    id_evaluation: int,
    id_comorbidite: int,
    payload: ComorbiditeEvaluationUpdate,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return evaluation_service.update_comorbidite(
        db, id_evaluation, id_comorbidite, payload, medecin.id_medecin
    )


@router.delete("/{id_evaluation}/comorbidites/{id_comorbidite}", status_code=204)
def remove_comorbidite(
    id_evaluation: int,
    id_comorbidite: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    evaluation_service.remove_comorbidite(db, id_evaluation, id_comorbidite, medecin.id_medecin)
