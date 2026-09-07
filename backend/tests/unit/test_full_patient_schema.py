from copy import deepcopy
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.full_patient import FullPatientCreate

VALID_PATIENT = {
    "nom": "Benali",
    "prenom": "Mohamed",
    "date_naissance": "1964-03-15",
    "sexe": "M",
    "telephone": "+212600000000",
    "email": "m.benali@example.com",
    "adresse": "123 Rue Principle, Casablanca",
    "antecedents": [
        {
            "degre_parente": "premier_degre",
            "nombre_apparentes": 1,
            "type_cancer": "pancreas",
        }
    ],
    "mutations": [
        {
            "id_gene": 1,
            "statut": "mute",
            "date_test": "2026-08-01T10:00:00",
        }
    ],
    "evaluation": {
        "date_evaluation": "2026-09-07",
        "contexte": "diagnostic",
        "ecog": 1,
        "etat_nutritionnel": "denutrition_moderee",
        "douleur_presente": True,
        "intensite_douleur": 5,
        "ictere": False,
        "diabete": "recent_moins_2ans",
        "biologie": {
            "ca19_9": "120.5",
            "ca19_9_multiple_lsn": None,
            "cholestase": True,
            "bilirubine": "38.2",
            "bilirubine_ratio_lsn": None,
            "statut_lewis": "exprime",
            "statut_dpd": "normal",
            "albuminemie": "32.0",
            "date_analyse": "2026-09-05",
        },
        "imageries": [
            {
                "type_imagerie": "TDM",
                "date_imagerie": "2026-09-03",
                "localisation_tumorale": "tete_crochet",
                "taille_tumorale_cm": "3.2",
                "contact_ams": "lt180",
                "contact_tronc_coeliaque": "absent",
                "contact_art_hepatique": "court_sans_envahissement",
                "contact_vms_vp": "absent",
                "extension_ganglionnaire_regionale": True,
                "extension_ganglionnaire_distance": False,
                "metastases_presentes": False,
                "metastases": [],
            }
        ],
        "histologie": {
            "preuve_histologique": True,
            "statut_brca_germinal": "non_teste",
            "statut_kras": "g12c",
            "statut_msi_dmmr": "mss",
            "fusion_ntrk": "non_teste",
            "fusion_nrg1": "non_teste",
        },
        "analyses": [
            {
                "type_test": "panel",
                "gene": "KRAS",
                "alteration": "G12C",
                "classe_escat": "I",
                "date_test": "2026-09-01",
                "reference_rapport": "RPT-2026-001",
            }
        ],
        "comorbidites": [
            {
                "id_comorbidite": 1,
                "severite": "mineure",
                "note": "Hypertension traitée",
            }
        ],
    },
}


def test_valid_full_patient():
    payload = FullPatientCreate.model_validate(VALID_PATIENT)

    assert payload.nom == "Benali"
    assert payload.sexe == "M"
    assert payload.evaluation.contexte == "diagnostic"
    assert payload.evaluation.biologie.ca19_9 == Decimal("120.5")
    assert payload.evaluation.imageries[0].type_imagerie == "TDM"
    assert payload.evaluation.histologie.statut_kras == "g12c"
    assert payload.evaluation.analyses[0].classe_escat == "I"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sexe", "string"),
        ("sexe", "inconnu_test"),
        ("sexe", ""),
    ],
)
def test_invalid_patient_enum(field, value):
    data = deepcopy(VALID_PATIENT)
    data[field] = value

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("contexte", "diagnositc"),
        ("contexte", "line_1"),
        ("etat_nutritionnel", "denutri"),
        ("diabete", "diabetique"),
    ],
)
def test_invalid_evaluation_enum(field, value):
    data = deepcopy(VALID_PATIENT)
    data["evaluation"][field] = value

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["ca19_9", "statut_lewis", "statut_dpd"],
)
def test_invalid_biologie(field):
    data = deepcopy(VALID_PATIENT)
    data["evaluation"]["biologie"][field] = "invalide"

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["type_imagerie", "localisation_tumorale", "contact_ams", "contact_tronc_coeliaque"],
)
def test_invalid_imagerie(field):
    data = deepcopy(VALID_PATIENT)
    data["evaluation"]["imageries"][0][field] = "invalide"

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["statut_brca_germinal", "statut_kras", "statut_msi_dmmr", "fusion_ntrk", "fusion_nrg1"],
)
def test_invalid_histologie(field):
    data = deepcopy(VALID_PATIENT)
    data["evaluation"]["histologie"][field] = "invalide"

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


def test_invalid_ecog_range():
    data = deepcopy(VALID_PATIENT)
    data["evaluation"]["ecog"] = 9

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


def test_invalid_intensite_douleur_range():
    data = deepcopy(VALID_PATIENT)
    data["evaluation"]["intensite_douleur"] = 11

    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate(data)


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        FullPatientCreate.model_validate({"nom": "Sans"})