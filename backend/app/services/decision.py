from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.decision import Decision
from app.models.evaluation import EvaluationClinique
from app.models.medecin import Medecin
from app.services.audit import log_action


def _not_found(msg: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


def decide(
    db: Session,
    id_evaluation: int,
    medecin: Medecin | None = None,
) -> Decision:
    """Crée une décision pour une évaluation."""
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None:
        raise _not_found(f"Évaluation {id_evaluation} introuvable.")

    decision = Decision(
        id_evaluation=evaluation.id_evaluation,
        decide_par=medecin.id_medecin if medecin else None,
        snapshot_patient=None,
        resume="Décision créée.",
        necessite_rcp=False,
    )
    db.add(decision)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de créer la décision (conflit de traçabilité).",
        )

    log_action(
        db,
        medecin_id=decision.decide_par,
        action="decision_create",
        type_entite="decision",
        id_entite=decision.id_decision,
        detail={"id_evaluation": id_evaluation},
    )

    db.commit()
    return get_decision_detail(db, decision.id_decision)


def get_decision(db: Session, id_decision: int) -> Decision:
    decision = db.get(Decision, id_decision)
    if decision is None:
        raise _not_found(f"Décision {id_decision} introuvable.")
    return decision


def get_decision_detail(db: Session, id_decision: int) -> Decision:
    return get_decision(db, id_decision)


def update_decision_medecin(
    db: Session,
    id_decision: int,
    decision_medecin: str,
    medecin: Medecin | None = None,
) -> Decision:
    """Enregistre la décision finale du médecin (ce qu'il a fait) sur une décision."""
    decision = get_decision(db, id_decision)
    decision.decision_medecin = decision_medecin
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


def list_decisions(db: Session, id_evaluation: int) -> list[Decision]:
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None:
        raise _not_found(f"Évaluation {id_evaluation} introuvable.")
    return (
        db.query(Decision)
        .filter(Decision.id_evaluation == id_evaluation)
        .order_by(Decision.date_decision.desc())
        .all()
    )
