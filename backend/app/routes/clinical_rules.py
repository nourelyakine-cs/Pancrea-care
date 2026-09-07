from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.clinical_rules import (
    ClinicalRulesCalculateRequest,
    DonneesDeriveesRead,
    RecommendationsResponse,
)
from app.services.clinical_rules.service import calculate_and_persist
from app.services.clinical_rules.recommendation_service import generate_recommendations
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/clinical-rules", tags=["clinical-rules"])


@router.post(
    "/evaluations/{id_evaluation}/calculate",
    response_model=DonneesDeriveesRead,
)
def calculate_clinical_rules(
    id_evaluation: int,
    payload: ClinicalRulesCalculateRequest,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return calculate_and_persist(db, id_evaluation, payload)


@router.get(
    "/evaluations/{id_evaluation}/recommendations",
    response_model=RecommendationsResponse,
)
def get_recommendations(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return generate_recommendations(db, id_evaluation)
