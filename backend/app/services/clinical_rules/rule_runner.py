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

# Champs affichés dans "criteres_evalues" à titre informatif pour les règles
# qui n'ont pas de pré-requis stricts dans _REQUIRED (R02 : conditions
# évaluées indépendamment ; R18 : chaque conclusion dépend d'un seul
# biomarqueur, vérifié indépendamment des autres).
# N'affecte jamais le calcul (pas utilisé pour décider si une règle est
# ignorée) : sert uniquement à enrichir la traçabilité renvoyée par l'API.
_DISPLAY_ONLY: dict[str, set[str]] = {
    "R02": {"resecabilite", "metastases", "ca19_9", "ecog"},
    "R18": {"fusion_ntrk", "fusion_nrg1", "statut_kras", "statut_msi_dmmr"},
}


def _r02_special_skip(facts: dict[str, Any]) -> bool:
    return facts.get("ca19_9") is None and facts.get("ecog") is None


def _criteria_fields(code: str) -> set[str]:
    return _REQUIRED.get(code) or _DISPLAY_ONLY.get(code, set())


def apply_safe(facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Apply rules while skipping rules whose required clinical inputs are unknown."""
    matched: list[dict[str, Any]] = []
    for code, fn, reference, grade in RULES:
        if code == "R02" and _r02_special_skip(facts):
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
                # Valeurs des faits utilisées pour déclencher cette règle :
                # sert de justification/traçabilité (cahier des charges).
                "criteres_evalues": {
                    name: facts.get(name) for name in sorted(_criteria_fields(code))
                },
            })
    return matched


def build_decision_path(facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Trace complète, dans l'ordre du moteur (R01→R18 puis T1→T4), de l'évaluation
    de CHAQUE règle : déclenchée, non déclenchée (conditions non remplies), ou
    ignorée (données manquantes).

    Répond à l'exigence du cahier des charges sur le « chemin de décision » :
    contrairement à `apply_safe` (qui ne renvoie que les règles déclenchées),
    cette fonction montre aussi ce qui a été vérifié et pourquoi une règle n'a
    pas produit de recommandation.
    """
    path: list[dict[str, Any]] = []
    for code, fn, reference, grade in RULES:
        required = _REQUIRED.get(code, set())
        missing = sorted(name for name in required if facts.get(name) is None)
        r02_skip = code == "R02" and _r02_special_skip(facts)

        if missing or r02_skip:
            path.append({
                "code": code,
                "statut": "ignoree",
                "motif": "donnees_manquantes",
                "champs_manquants": missing or ["ca19_9", "ecog"],
            })
            continue

        result = fn(facts)
        conclusions = result if isinstance(result, list) else ([result] if result else [])
        path.append({
            "code": code,
            "statut": "declenchee" if conclusions else "non_declenchee",
            "reference": reference,
            "grade": grade,
            "criteres_evalues": {
                name: facts.get(name) for name in sorted(_criteria_fields(code))
            },
            "nombre_conclusions": len(conclusions),
        })
    return path
