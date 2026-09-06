"""Tests unitaires pour `_patient_non_operable` (règle R03).

Règle : patient_non_operable = True si comorbidites_lourdes=True
OU etat_nutritionnel='denutrition_severe' OU ecog >= 3, False sinon,
None si aucun critère n'est positif mais qu'une donnée nécessaire manque.

Ce module fixe des variables d'environnement factices AVANT d'importer
`app.services.clinical_rules.facts`, car ce module importe (en cascade)
`app.database` -> `app.config`, qui exige DATABASE_URL / SUPABASE_URL /
SUPABASE_ANON_KEY. `_patient_non_operable` elle-même n'a aucune dépendance
DB : c'est une fonction pure.
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")

from app.services.clinical_rules.facts import _patient_non_operable  # noqa: E402


def test_true_when_comorbidites_lourdes():
    assert _patient_non_operable(True, "normal", 1) is True


def test_true_when_denutrition_severe():
    assert _patient_non_operable(False, "denutrition_severe", 0) is True


def test_true_when_ecog_ge_3():
    assert _patient_non_operable(False, "normal", 3) is True
    assert _patient_non_operable(False, "normal", 4) is True


def test_false_when_all_criteria_known_and_negative():
    assert _patient_non_operable(False, "normal", 1) is False
    assert _patient_non_operable(False, "denutrition_moderee", 2) is False


def test_unknown_when_ecog_missing_and_nothing_positive():
    assert _patient_non_operable(False, "normal", None) is None


def test_unknown_when_etat_nutritionnel_missing_or_non_renseigne():
    assert _patient_non_operable(False, None, 1) is None
    assert _patient_non_operable(False, "inconnu", 1) is None


def test_unknown_when_everything_missing():
    assert _patient_non_operable(False, None, None) is None


def test_positive_criterion_wins_even_if_others_unknown():
    # Un seul critère positif suffit à conclure True, peu importe le reste.
    assert _patient_non_operable(True, None, None) is True
