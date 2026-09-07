from __future__ import annotations

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.evaluation import Biologie, EvaluationClinique, Imagerie
from app.schemas.clinical_rules import ClinicalRulesCalculateRequest

from .adapters import (
    biology_to_engine_input,
    db_resecabilite_value,
    image_to_engine_input,
    parse_tnm,
)
from .resecabilite_vasculaire import evaluer_resecabilite_vasculaire
from .staging_tnm_criteres_abc import calculer_criteres_abc, calculer_stade_tnm


def _latest_image(db: Session, id_evaluation: int) -> Imagerie:
    image = (
        db.query(Imagerie)
        .filter(Imagerie.id_evaluation == id_evaluation)
        .order_by(Imagerie.date_imagerie.desc(), Imagerie.id_imagerie.desc())
        .first()
    )
    if image is None:
        raise HTTPException(status_code=422, detail="Aucune imagerie disponible pour cette évaluation")
    return image


def calculate_and_persist(
    db: Session,
    id_evaluation: int,
    payload: ClinicalRulesCalculateRequest,
) -> DonneesDerivees:
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None:
        raise HTTPException(status_code=404, detail=f"Évaluation {id_evaluation} introuvable")

    image = _latest_image(db, id_evaluation)
    biology = (
        db.query(Biologie)
        .filter(Biologie.id_evaluation == id_evaluation)
        .first()
    )

    try:
        vascular_input = image_to_engine_input(image)
        abc_input = biology_to_engine_input(evaluation, biology)
        m_value = payload.categorie_m
        if m_value is None:
            m_value = "M1" if image.metastases_presentes else "M0"
        t, n, m = parse_tnm(payload.categorie_t, payload.categorie_n, m_value)
        vascular = evaluer_resecabilite_vasculaire(vascular_input)
        tnm = calculer_stade_tnm(t, n, m)
        abc = calculer_criteres_abc(abc_input)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    db_status = db_resecabilite_value(vascular.statut_global.value)
    derived = (
        db.query(DonneesDerivees)
        .filter(
            DonneesDerivees.id_evaluation == id_evaluation,
            DonneesDerivees.version_moteur == payload.version_moteur,
        )
        .first()
    )
    values = {
        "id_evaluation": id_evaluation,
        "version_moteur": payload.version_moteur,
        "source_code": "TNCD-2024",
        "source_version": "17/05/2024",
        "resecabilite": db_status,
        "categorie_t": t.value,
        "categorie_n": n.value,
        "categorie_m": m.value,
        "stade_global": tnm.stade_global.value,
        "critere_abc_a": db_status,
        "critere_abc_b": abc.critere_B_positif,
        "critere_abc_c": abc.critere_C_positif,
        "sous_categorie_abc": f"{db_status}_{abc.type_abc}",
        "justification_calcul": json.dumps(
            {
                "resecabilite": vascular.model_dump(mode="json"),
                "tnm": tnm.model_dump(mode="json"),
                "abc": abc.model_dump(mode="json"),
            },
            ensure_ascii=False,
        ),
    }
    if derived is None:
        derived = DonneesDerivees(**values)
        db.add(derived)
    else:
        for key, value in values.items():
            if key != "id_evaluation":
                setattr(derived, key, value)
    db.commit()
    db.refresh(derived)
    return derived
