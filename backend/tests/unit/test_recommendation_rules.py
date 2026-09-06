from app.services.clinical_rules.rule_runner import apply_safe


def base_facts():
    return {
        "resecabilite": "resecable",
        "metastases": False,
        "adenopathie_distance": False,
        "ca19_9": 300,
        "ecog": 1,
    }


def test_r01_matches_ideal_resectable_profile():
    matches = apply_safe(base_facts())
    assert any(item["code"] == "R01" for item in matches)


def test_r01_does_not_match_when_critical_ca19_is_unknown():
    facts = base_facts()
    facts["ca19_9"] = None
    matches = apply_safe(facts)
    assert not any(item["code"] == "R01" for item in matches)


def test_r11_does_not_assume_unknown_bilirubin_is_normal():
    facts = {
        "metastases": True,
        "age": 60,
        "ecog": 0,
        "bilirubine_ratio_lsn": None,
    }
    matches = apply_safe(facts)
    assert not any(item["code"] == "R11" for item in matches)


def test_r15_requires_metastatic_status():
    facts = {
        "ligne_precedente": "gemcitabine",
        "reponse_traitement": "progression",
        "ecog": 0,
        "metastases": None,
    }
    matches = apply_safe(facts)
    assert not any(item["code"] == "R15" for item in matches)
