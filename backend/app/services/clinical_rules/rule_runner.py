from __future__ import annotations

from typing import Any

from .recommendation_rules import RULES

_REQUIRED: dict[str, set[str]] = {
    "R01": {"resecabilite", "metastases", "adenopathie_distance", "ecog"},
    "R02": {"resecabilite", "metastases", "critere_abc_b", "critere_abc_c"},
    "R03": {"resecabilite", "patient_non_operable"},
    "R04": {"resecabilite", "metastases"},
    "R05": {"resecabilite", "tumeur_controlee", "nouvelles_metastases"},
    "R06": {"resecabilite", "metastases", "ecog"}, "R07": {"resecabilite", "metastases", "ecog"},
    "R08": {"resecabilite", "metastases", "ecog"}, "R09": {"resecabilite", "metastases", "tumeur_controlee", "duree_chimiotherapie_mois"},
    "R10": {"metastases", "ecog"}, "R11": {"metastases", "age", "ecog", "bilirubine_ratio_lsn"},
    "R12": {"metastases", "age", "ecog", "bilirubine_ratio_lsn"}, "R13": {"metastases", "ecog", "bilirubine_ratio_lsn"},
    "R14": {"metastases", "statut_brca", "pas_de_progression_apres_16_semaines_platine"},
    "R15": {"metastases", "ligne_precedente", "reponse_traitement", "ecog"},
    "R16": {"metastases", "ligne_precedente", "reponse_traitement", "ecog"},
    "R17": {"ligne_traitement_actuelle", "ecog"}, "T1": {"ictere", "angiocholite", "bilirubine"},
    "T2": {"adenopathie_distance"}, "T3": {"statut_dpd"}, "T4": {"traitement_medical_prevu", "chirurgie_d_emblee", "preuve_histologique"},
}
_DISPLAY_ONLY = {"R18": {"fusion_ntrk", "fusion_nrg1", "statut_kras", "statut_msi_dmmr"}}


def _criteria_fields(code: str) -> set[str]:
    return _REQUIRED.get(code) or _DISPLAY_ONLY.get(code, set())


def _flat(result: Any) -> list[Any]:
    if isinstance(result, list):
        return result
    return [result] if result else []


def apply_safe(facts: dict[str, Any]) -> list[dict[str, Any]]:
    matched = []
    for code, fn, reference, grade in RULES:
        required = _REQUIRED.get(code, set())
        if any(facts.get(name) is None for name in required):
            continue
        for conclusion in _flat(fn(facts)):
            matched.append({"code": code, "conclusion": conclusion, "reference": reference, "grade": grade, "criteres_evalues": {name: facts.get(name) for name in sorted(_criteria_fields(code))}})
    return matched


def build_decision_path(facts: dict[str, Any]) -> list[dict[str, Any]]:
    path = []
    for code, fn, reference, grade in RULES:
        required = _REQUIRED.get(code, set())
        missing = sorted(name for name in required if facts.get(name) is None)
        if missing:
            path.append({"code": code, "statut": "ignoree", "motif": "donnees_manquantes", "champs_manquants": missing})
            continue
        conclusions = _flat(fn(facts))
        path.append({"code": code, "statut": "declenchee" if conclusions else "non_declenchee", "reference": reference, "grade": grade, "criteres_evalues": {name: facts.get(name) for name in sorted(_criteria_fields(code))}, "nombre_conclusions": len(conclusions)})
    return path
