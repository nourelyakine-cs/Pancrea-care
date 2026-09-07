from typing import Any


def _num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def r01(facts: dict[str, Any]) -> str | None:
    if (
        facts.get("resecabilite") == "resecable"
        and facts.get("metastases") is False
        and facts.get("adenopathie_distance") is False
        and (facts.get("ca19_9") is None or (_num(facts.get("ca19_9")) is not None and _num(facts.get("ca19_9")) <= 500))
        and facts.get("ecog") in (0, 1)
    ):
        return "Discuter en RCP une chirurgie à visée curative (DPC ou SPG selon localisation) dans un centre expert. En l'absence de contre-indication, prévoir une chimiothérapie adjuvante de 6 mois, mFOLFIRINOX en 1ère intention si l'état général et les comorbidités le permettent."
    return None


def r02(facts: dict[str, Any]) -> str | None:
    if (
        facts.get("resecabilite") == "resecable"
        and facts.get("metastases") is False
        and (facts.get("critere_abc_b") is True or facts.get("critere_abc_c") is True)
    ):
        return "Tumeur anatomiquement résécable mais avec critères défavorables (CA19-9 élevé et/ou état général altéré). Discuter en RCP une chimiothérapie néoadjuvante avant chirurgie (option, avis d'experts)."
    return None


def r03(facts):
    if facts.get("resecabilite") == "resecable" and facts.get("patient_non_operable") is True:
        return "Tumeur anatomiquement résécable mais patient jugé non opérable (comorbidités lourdes, dénutrition sévère et/ou ECOG ≥ 3). Ne pas recommander de chirurgie première ; orienter vers une prise en charge médicale similaire aux tumeurs localement avancées."
    return None


def r04(facts):
    if facts.get("resecabilite") == "borderline" and facts.get("metastases") is False:
        return "Tumeur à la limite de la résécabilité (borderline). Privilégier un traitement d'induction, idéalement dans un essai clinique."
    return None


def r05(facts):
    if facts.get("resecabilite") == "borderline" and facts.get("tumeur_controlee") is True and facts.get("nouvelles_metastases") is False:
        return "En cas de bonne réponse après induction, proposer en option une chimioradiothérapie pré-opératoire avec capécitabine avant chirurgie, à discuter en RCP."
    return None


def r06(facts):
    if facts.get("resecabilite") == "localement_avance" and facts.get("metastases") is False and facts.get("ecog") in (0, 1):
        return "Tumeur localement avancée, bon état général. Chimiothérapie d'induction par mFOLFIRINOX ou gemcitabine + nab-paclitaxel selon le profil."
    return None


def r07(facts):
    if facts.get("resecabilite") == "localement_avance" and facts.get("metastases") is False and facts.get("ecog") == 2:
        return "Tumeur localement avancée, état général intermédiaire. Chimiothérapie d'induction par gemcitabine seule."
    return None


def r08(facts):
    if facts.get("resecabilite") == "localement_avance" and facts.get("metastases") is False and facts.get("ecog") is not None and facts.get("ecog") >= 3:
        return "Tumeur localement avancée, état général très altéré. Privilégier les soins de support."
    return None


def r09(facts):
    if facts.get("resecabilite") == "localement_avance" and facts.get("metastases") is False and facts.get("tumeur_controlee") is True and (_num(facts.get("duree_chimiotherapie_mois")) or 0) >= 4:
        return "Discuter une chimioradiothérapie de clôture avec capécitabine après induction et une réévaluation chirurgicale en cas de très bonne réponse."
    return None


def r10(facts):
    if facts.get("metastases") is True and facts.get("ecog") in (3, 4):
        return "Maladie métastatique, état général très altéré. Privilégier les soins de support."
    return None


def r11(facts):
    if facts.get("metastases") is True and _num(facts.get("age")) is not None and _num(facts.get("age")) < 75 and facts.get("ecog") in (0, 1) and _num(facts.get("bilirubine_ratio_lsn")) is not None and _num(facts.get("bilirubine_ratio_lsn")) < 1.5:
        return "Maladie métastatique, bon état général, âge < 75 ans, bilirubine normale. Chimiothérapie de 1ère ligne par FOLFIRINOX ou mFOLFIRINOX."
    return None


def r12(facts):
    if facts.get("metastases") is True and (facts.get("ecog") == 2 or (_num(facts.get("age")) is not None and _num(facts.get("age")) >= 75)) and _num(facts.get("bilirubine_ratio_lsn")) is not None and _num(facts.get("bilirubine_ratio_lsn")) < 1.5:
        return "Maladie métastatique, ECOG 2 ou âge ≥ 75 ans, bilirubine normale. Chimiothérapie de 1ère ligne par gemcitabine seule."
    return None


def r13(facts):
    if facts.get("metastases") is True and facts.get("ecog") in (0, 1, 2) and _num(facts.get("bilirubine_ratio_lsn")) is not None and _num(facts.get("bilirubine_ratio_lsn")) >= 1.5:
        return "Maladie métastatique, bilirubine élevée. Privilégier la gemcitabine seule après évaluation d'un éventuel drainage biliaire."
    return None


def r14(facts):
    if facts.get("metastases") is True and facts.get("statut_brca") == "mute" and facts.get("pas_de_progression_apres_16_semaines_platine") is True:
        return "Maladie métastatique avec mutation germinale BRCA1/2, sans progression après ≥ 16 semaines de platine. Proposer olaparib en maintenance."
    return None


def r15(facts):
    if facts.get("metastases") is True and facts.get("ligne_precedente") == "gemcitabine" and facts.get("reponse_traitement") == "progression" and facts.get("ecog") in (0, 1):
        return "Progression après gemcitabine en 1ère ligne. Chimiothérapie de 2ème ligne par 5-FU + nal-IRI ou 5-FU + oxaliplatine."
    return None


def r16(facts):
    if facts.get("metastases") is True and facts.get("ligne_precedente") == "folfirinox" and facts.get("reponse_traitement") == "progression" and facts.get("ecog") in (0, 1):
        return "Progression après FOLFIRINOX en 1ère ligne. Chimiothérapie de 2ème ligne par gemcitabine seule ou gemcitabine + paclitaxel."
    return None


def r17(facts):
    if (_num(facts.get("ligne_traitement_actuelle")) or 0) >= 3 and facts.get("ecog") in (0, 1):
        return "Maladie métastatique en 3ème ligne ou au-delà, bon état général. Privilégier l'inclusion en essai clinique et la discussion en RCP moléculaire."
    return None


def r18(facts):
    out = []
    if facts.get("fusion_ntrk") == "positif":
        out.append("Proposer larotrectinib, selon disponibilité et RCP.")
    if facts.get("fusion_nrg1") == "positif":
        out.append("Proposer zenocutuzumab, à discuter en RCP moléculaire.")
    if facts.get("statut_kras") == "g12c":
        out.append("Proposer adagrasib ou sotorasib, à discuter en RCP moléculaire.")
    if facts.get("statut_msi_dmmr") in {"msi_h", "dmmr"}:
        out.append("Proposer une immunothérapie, à discuter en RCP moléculaire (MSI-H/dMMR).")
    return out


def t1(facts):
    if facts.get("ictere") is True and (facts.get("angiocholite") is True or ((_num(facts.get("bilirubine")) or 0) > 250)):
        return "Ictère avec angiocholite et/ou bilirubine très élevée. Proposer un drainage biliaire en urgence."
    return None


def t2(facts):
    if facts.get("adenopathie_distance") is True:
        return "Adénopathie à distance documentée. Contre-indication à une chirurgie première."
    return None


def t3(facts):
    if facts.get("statut_dpd") == "deficit_complet":
        return "Déficit complet en DPD : contre-indication au 5-FU et à la capécitabine."
    if facts.get("statut_dpd") == "deficit_partiel":
        return "Déficit partiel en DPD : ajustement de dose recommandé."
    return None


def t4(facts):
    if facts.get("traitement_medical_prevu") is True and facts.get("chirurgie_d_emblee") is False and facts.get("preuve_histologique") is not True:
        return "Traitement médical prévu sans chirurgie d'emblée : obtenir une preuve histologique avant le traitement."
    return None


REFERENCE = {
    "R01": ("TNCD 9.4.1.1 / 9.4.1.3", "A"), "R02": ("TNCD 9.2.2.2 / 9.4.1.4", "accord_experts"),
    "R03": ("TNCD 9.2.6.1 / 9.4.1.1", "accord_experts"), "R04": ("TNCD 9.4.2.1", "B"),
    "R05": ("TNCD 9.4.2.1", "accord_experts"), "R06": ("TNCD 9.4.3.1", "A"),
    "R07": ("TNCD 9.4.3.1", "A"), "R08": ("TNCD 9.2.6.2 / 9.4.3", "accord_experts"),
    "R09": ("TNCD 9.4.3.2 / 9.4.3.3", "B"), "R10": ("TNCD 9.2.6.2 / 9.4.4", "accord_experts"),
    "R11": ("TNCD 9.4.4.1", "A"), "R12": ("TNCD 9.4.4.1", "A"), "R13": ("TNCD 9.4.4.1", "A"),
    "R14": ("TNCD 9.4.5", "B"), "R15": ("TNCD 9.4.4.2", "A"), "R16": ("TNCD 9.4.4.2", "B"),
    "R17": ("TNCD 9.4.5", "accord_experts"), "R18": ("TNCD 9.4.5", "B"),
    "T1": ("TNCD 9.2.3.4", "A"), "T2": ("TNCD 9.2.5 / 9.4.1.1", "accord_experts"),
    "T3": ("TNCD 9.2.7.1", "A"), "T4": ("TNCD 9.2.4 / 9.2.7.2", "A"),
}

RULES = [(code, globals()[code.lower()], *REFERENCE[code]) for code in REFERENCE]
