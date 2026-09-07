from types import SimpleNamespace

import pytest

from app.services.clinical_rules.adapters import (
    db_resecabilite_value,
    image_to_engine_input,
    parse_tnm,
)


def complete_image(**overrides):
    values = dict(
        contact_ams="absent",
        contact_tronc_coeliaque="absent",
        contact_art_hepatique="absent",
        contact_vms_vp="absent",
        extension_ganglionnaire_distance=False,
        metastases_presentes=False,
        localisation_tumorale="tete_crochet",
    )
    values.update(overrides)
    return SimpleNamespace(**values)


def test_sql_values_are_converted_to_engine_input():
    result = image_to_engine_input(
        complete_image(contact_ams="lt180", contact_vms_vp="ge180_ou_irregularite")
    )
    assert result.ams.circonference_ge_180 is False
    assert result.vms_vp.circonference_ge_180 is True


def test_critical_null_is_not_treated_as_false():
    with pytest.raises(ValueError, match="metastases_presentes"):
        image_to_engine_input(complete_image(metastases_presentes=None))


def test_unknown_tnm_is_rejected_before_staging():
    with pytest.raises(ValueError, match="TX"):
        parse_tnm("TX", "N0", "M0")
    with pytest.raises(ValueError, match="NX"):
        parse_tnm("T2", "NX", "M0")


def test_metastatic_status_matches_database_enum():
    assert db_resecabilite_value("non_pertinent_metastatique") == "metastatique"
    assert db_resecabilite_value("borderline") == "borderline"
