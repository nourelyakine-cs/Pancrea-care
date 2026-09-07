from app.services.clinical_rules.rule_runner import apply_safe


def test_r01_allows_missing_ca19_9():
    facts = {"resecabilite": "resecable", "metastases": False, "adenopathie_distance": False, "ca19_9": None, "ecog": 1}
    assert any(item["code"] == "R01" for item in apply_safe(facts))


def test_r02_uses_derived_abc_and_does_not_recalculate_cholestasis():
    facts = {"resecabilite": "resecable", "metastases": False, "critere_abc_b": False, "critere_abc_c": False, "ca19_9": 620, "cholestase": True, "ecog": 1}
    assert not any(item["code"] == "R02" for item in apply_safe(facts))


def test_r02_matches_when_derived_criterion_b_or_c_is_true():
    base = {"resecabilite": "resecable", "metastases": False, "critere_abc_b": True, "critere_abc_c": False}
    assert any(item["code"] == "R02" for item in apply_safe(base))
    base["critere_abc_b"] = False
    base["critere_abc_c"] = True
    assert any(item["code"] == "R02" for item in apply_safe(base))


def test_r18_msi_h_and_dmmr_trigger_immunotherapy():
    for status in ("msi_h", "dmmr"):
        matches = apply_safe({"fusion_ntrk": None, "fusion_nrg1": None, "statut_kras": None, "statut_msi_dmmr": status})
        assert any(item["code"] == "R18" for item in matches)


def test_r18_mss_does_not_trigger_immunotherapy():
    matches = apply_safe({"fusion_ntrk": None, "fusion_nrg1": None, "statut_kras": None, "statut_msi_dmmr": "mss"})
    assert not any(item["code"] == "R18" for item in matches)
