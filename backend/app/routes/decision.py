from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medecin import Medecin
from app.schemas.decision import DecisionDetailRead, DecisionRead
from app.services import decision as decision_service
from app.supabase import get_medecin_for_user

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post("/evaluations/{id_evaluation}/decide", response_model=DecisionDetailRead, status_code=201)
def decide(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return decision_service.decide(db, id_evaluation, medecin)


@router.get("/evaluations/{id_evaluation}", response_model=list[DecisionRead])
def list_decisions(
    id_evaluation: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return decision_service.list_decisions(db, id_evaluation)


@router.get("/{id_decision}", response_model=DecisionDetailRead)
def get_decision(
    id_decision: int,
    medecin: Medecin = Depends(get_medecin_for_user),
    db: Session = Depends(get_db),
):
    return decision_service.get_decision_detail(db, id_decision)
