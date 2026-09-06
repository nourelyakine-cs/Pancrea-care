from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.evaluation import (
    Biologie,
    EvaluationClinique,
    HistologieBiologie,
    Imagerie,
)

from .facts import build_rule_facts
from .rule_runner import apply_safe, build_decision_path


def _load_context(db: Session, id_evaluation: int):
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None:
        raise HTTPException(status_code=404, detail=f"Évaluation {id_evaluation} introuvable")
    image = (
        db.query(Imagerie)
        .filter(Imagerie.id_evaluation == id_evaluation)
        .order_by(Imagerie.date_imagerie.desc(), Imagerie.id_imagerie.desc())
        .first()
    )
    if image is None:
        raise HTTPException(status_code=422, detail="Aucune imagerie disponible")
    derived = (
        db.query(DonneesDerivees)
        .filter(DonneesDerivees.id_evaluation == id_evaluation)
        .order_by(DonneesDerivees.date_calcul.desc(), DonneesDerivees.id_derive.desc())
        .first()
    )
    if derived is None:
        raise HTTPException(
            status_code=422,
            detail="Calcul vascular/TNM/ABC requis avant les recommandations",
        )
    biology = db.query(Biologie).filter(Biologie.id_evaluation == id_evaluation).first()
    histology = (
        db.query(HistologieBiologie)
        .filter(HistologieBiologie.id_evaluation == id_evaluation)
        .first()
    )
    return evaluation, derived, biology, image, histology


def generate_recommendations(db: Session, id_evaluation: int) -> dict[str, Any]:
    evaluation, derived, biology, image, histology = _load_context(db, id_evaluation)
    facts = build_rule_facts(db, evaluation, derived, biology, image, histology)
    recommendations = apply_safe(facts)
    return {
        "facts": facts,
        "recommendations": recommendations,
        # Liste explicite des codes de règles déclenchées (R01-R18, T1-T4...),
        # exigée par le cahier des charges en plus du détail dans "recommendations".
        "regles_declenchees": [item["code"] for item in recommendations],
        # Chemin de décision : trace ordonnée de TOUTES les règles évaluées
        # (déclenchées, non déclenchées, ou ignorées faute de données), avec
        # les critères examinés pour chacune.
        "decision_path": build_decision_path(facts),
    }
