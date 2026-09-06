from __future__ import annotations

from typing import Any

from .recommendation_rules import RULES

_REQUIRED: dict[str, set[str]] = {
    "R01": {"resecabilite", "metastases", "adenopathie_distance", "ca19_9", "ecog"},
    "R03": {"resecabilite", "patient_non_operable"},
    "R04": {"resecabilite", "metastases"},
    "R05": {"resecabilite", "tumeur_controlee", "nouvelles_metastases"},
    "R06": {"resecabilite", "metastases", "ecog"},
    "R07": {"resecabilite", "metastases", "ecog"},
    "R08": {"resecabilite", "metastases", "ecog"},
    "R09": {"resecabilite", "metastases", "tumeur_controlee", "duree_chimiotherapie_mois"},
    "R10": {"metastases", "ecog"},
    "R11": {"metastases", "age", "ecog", "bilirubine_ratio_lsn"},
    "R12": {"metastases", "age", "ecog", "bilirubine_ratio_lsn"},
    "R13": {"metastases", "ecog", "bilirubine_ratio_lsn"},
    "R14": {"metastases", "statut_brca", "pas_de_progression_apres_16_semaines_platine"},
    "R15": {"metastases", "ligne_precedente", "reponse_traitement", "ecog"},
    "R16": {"metastases", "ligne_precedente", "reponse_traitement", "ecog"},
    "R17": {"ligne_traitement_actuelle", "ecog"},
    "T1": {"ictere", "angiocholite", "bilirubine"},
    "T2": {"adenopathie_distance"},
    "T3": {"statut_dpd"},
    "T4": {"traitement_medical_prevu", "chirurgie_d_emblee"},
}


def apply_safe(facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Apply rules while skipping rules whose required clinical inputs are unknown."""
    matched: list[dict[str, Any]] = []
    for code, fn, reference, grade in RULES:
        if code == "R02" and facts.get("ca19_9") is None and facts.get("ecog") is None:
            continue
        required = _REQUIRED.get(code, set())
        if any(facts.get(name) is None for name in required):
            continue
        result = fn(facts)
        conclusions = result if isinstance(result, list) else ([result] if result else [])
        for conclusion in conclusions:
            matched.append({
                "code": code,
                "conclusion": conclusion,
                "reference": reference,
                "grade": grade,
            })
    return matched
