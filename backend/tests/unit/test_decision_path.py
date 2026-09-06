"""Tests unitaires pour la traçabilité/explicabilité du moteur de règles :
- `apply_safe` doit renvoyer, pour chaque recommandation, les critères
  (faits) qui l'ont déclenchée (`criteres_evalues`).
- `build_decision_path` doit renvoyer, dans l'ordre du moteur, le résultat
  de l'évaluation de CHAQUE règle (déclenchée / non déclenchée / ignorée).
"""

from app.services.clinical_rules.rule_runner import apply_safe, build_decision_path

IDEAL_RESECTABLE_FACTS = {
    "resecabilite": "resecable",
    "metastases": False,
    "adenopathie_distance": False,
    "ca19_9": 300,
    "ecog": 1,
}


def test_apply_safe_exposes_the_criteria_that_triggered_the_rule():
    matches = apply_safe(IDEAL_RESECTABLE_FACTS)
    r01 = next(item for item in matches if item["code"] == "R01")
    assert r01["criteres_evalues"]["resecabilite"] == "resecable"
    assert r01["criteres_evalues"]["ecog"] == 1
    assert r01["criteres_evalues"]["ca19_9"] == 300


def test_decision_path_covers_every_rule_in_engine_order():
    path = build_decision_path(IDEAL_RESECTABLE_FACTS)
    codes = [step["code"] for step in path]
    assert codes[0] == "R01"
    assert codes[-1] == "T4"
    assert codes.count("R01") == 1
    assert len(codes) == len(set(codes))  # chaque règle apparaît une seule fois


def test_decision_path_marks_matching_rule_as_declenchee():
    path = build_decision_path(IDEAL_RESECTABLE_FACTS)
    r01_step = next(step for step in path if step["code"] == "R01")
    assert r01_step["statut"] == "declenchee"
    assert r01_step["nombre_conclusions"] == 1


def test_decision_path_flags_missing_data_with_the_missing_fields():
    facts = {"resecabilite": "resecable"}  # metastases, ca19_9, ecog... manquants
    path = build_decision_path(facts)
    r01_step = next(step for step in path if step["code"] == "R01")
    assert r01_step["statut"] == "ignoree"
    assert r01_step["motif"] == "donnees_manquantes"
    assert "ecog" in r01_step["champs_manquants"]
    assert "metastases" in r01_step["champs_manquants"]


def test_decision_path_marks_non_matching_rule_as_non_declenchee():
    # Toutes les données R01 sont connues, mais CA19-9 > 500 -> R01 ne matche pas.
    facts = dict(IDEAL_RESECTABLE_FACTS, ca19_9=800)
    path = build_decision_path(facts)
    r01_step = next(step for step in path if step["code"] == "R01")
    assert r01_step["statut"] == "non_declenchee"
    assert r01_step["nombre_conclusions"] == 0
