from typing import Any, Callable


def _num(value: Any) -> float | None:
    """Coerce en float, ou None si absent/invalide."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# --- Situation « résécable / borderline » -------------------------------

def r01(facts: dict[str, Any]) -> str | None:
    """Résécable, profil idéal → chirurgie d'emblée + adjuvante."""
    if (
        facts.get("resecabilite") == "resecable"
        and not facts.get("metastases")
        and not facts.get("adenopathie_distance")
        and (_num(facts.get("ca19_9")) or 0) <= 500
        and facts.get("ecog") in (0, 1)
    ):
        return (
            "Discuter en RCP une chirurgie à visée curative (DPC ou SPG selon "
            "localisation) dans un centre expert. En l'absence de contre-indication, "
            "prévoir une chimiothérapie adjuvante de 6 mois, mFOLFIRINOX en 1ère "
            "intention si l'état général et les comorbidités le permettent."
        )
    return None


def r02(facts: dict[str, Any]) -> str | None:
    """Résécable avec critères défavorables (CA19-9 élevé et/ou ECOG ≥ 2) → néoadjuvant."""
    if (
        facts.get("resecabilite") == "resecable"
        and not facts.get("metastases")
        and (_num(facts.get("ca19_9")) or 0) > 500
    ):
        return (
            "Tumeur anatomiquement résécable mais avec critères défavorables "
            "(CA19-9 élevé). Discuter en RCP une chimiothérapie néoadjuvante avant "
            "chirurgie (option, avis d'experts)."
        )
    if (
        facts.get("resecabilite") == "resecable"
        and not facts.get("metastases")
        and facts.get("ecog") is not None
        and facts.get("ecog") >= 2
    ):
        return (
            "Tumeur anatomiquement résécable mais état général altéré (ECOG ≥ 2). "
            "Discuter en RCP une chimiothérapie néoadjuvante avant chirurgie "
            "(option, avis d'experts)."
        )
    return None


def r03(facts: dict[str, Any]) -> str | None:
    """Résécable mais patient non opérable → prise en charge comme LA."""
    if (
        facts.get("resecabilite") == "resecable"
        and facts.get("patient_non_operable")
    ):
        return (
            "Tumeur anatomiquement résécable mais patient jugé non opérable "
            "(comorbidités lourdes, dénutrition sévère et/ou ECOG ≥ 3). Ne pas "
            "recommander de chirurgie première ; orienter vers une prise en charge "
            "médicale (chimiothérapie ± soins de support) similaire aux tumeurs "
            "localement avancées."
        )
    return None


def r04(facts: dict[str, Any]) -> str | None:
    """Borderline, sans métastase → traitement d'induction puis réévaluation."""
    if (
        facts.get("resecabilite") == "borderline"
        and not facts.get("metastases")
    ):
        return (
            "Tumeur à la limite de la résécabilité (borderline). Privilégier un "
            "traitement d'induction (ex. mFOLFIRINOX ou gemcitabine + nab-paclitaxel), "
            "idéalement dans un essai clinique. Réévaluer : discuter chirurgie "
            "secondaire si contrôle et absence de nouvelles métastases (puis "
            "adjuvante ~6 mois) ; sinon orienter vers une prise en charge "
            "avancée/métastatique."
        )
    return None


def r05(facts: dict[str, Any]) -> str | None:
    """Borderline, bonne réponse après induction → option chimioradiothérapie pré-op."""
    if (
        facts.get("resecabilite") == "borderline"
        and facts.get("tumeur_controlee")
        and not facts.get("nouvelles_metastases")
    ):
        return (
            "Bonnes réponses après induction : proposer en option une "
            "chimioradiothérapie pré-opératoire (avec capécitabine) avant chirurgie, "
            "à discuter en RCP (essais cliniques, avis d'experts)."
        )
    return None


# --- Situation « localement avancé » ------------------------------------

def r06(facts: dict[str, Any]) -> str | None:
    """Localement avancé, ECOG 0-1 → induction intensive."""
    if (
        facts.get("resecabilite") == "localement_avance"
        and not facts.get("metastases")
        and facts.get("ecog") in (0, 1)
    ):
        return (
            "Tumeur localement avancée, bon état général. Chimiothérapie d'induction "
            "par mFOLFIRINOX (ou gemcitabine + nab-paclitaxel selon profil et centre)."
        )
    return None


def r07(facts: dict[str, Any]) -> str | None:
    """Localement avancé, ECOG 2 → gemcitabine."""
    if (
        facts.get("resecabilite") == "localement_avance"
        and not facts.get("metastases")
        and facts.get("ecog") == 2
    ):
        return (
            "Tumeur localement avancée, état général intermédiaire (ECOG 2). "
            "Chimiothérapie d'induction par gemcitabine seule (option : "
            "gemcitabine + nab-paclitaxel si bon état général et centre expert)."
        )
    return None


def r08(facts: dict[str, Any]) -> str | None:
    """Localement avancé, ECOG ≥ 3 → soins de support."""
    if (
        facts.get("resecabilite") == "localement_avance"
        and not facts.get("metastases")
        and facts.get("ecog") is not None
        and facts.get("ecog") >= 3
    ):
        return (
            "Tumeur localement avancée, état général très altéré (ECOG ≥ 3). "
            "Privilégier les soins de support ; chimiothérapie systémique "
            "généralement non recommandée, sauf cas très sélectionnés et discussion RCP."
        )
    return None


def r09(facts: dict[str, Any]) -> str | None:
    """Localement avancé contrôlé ≥ 4 mois → CRT de clôture et/ou réévaluation chirurgicale."""
    if (
        facts.get("resecabilite") == "localement_avance"
        and not facts.get("metastases")
        and facts.get("tumeur_controlee")
        and (_num(facts.get("duree_chimiotherapie_mois")) or 0) >= 4
    ):
        return (
            "Discuter une chimioradiothérapie de clôture (avec capécitabine) après "
            "induction, à décider en RCP. Réévaluation chirurgicale en cas de très "
            "bonne réponse (clinique, imagerie, CA19-9), dans un centre expert."
        )
    return None


# --- Situation « métastatique » — 1ère ligne ----------------------------

def r10(facts: dict[str, Any]) -> str | None:
    """Métastatique, ECOG 3-4 → soins de support."""
    if (
        facts.get("metastases")
        and facts.get("ecog") in (3, 4)
    ):
        return (
            "Maladie métastatique, état général très altéré (ECOG 3-4). Privilégier "
            "les soins de support ; chimiothérapie systémique généralement non recommandée."
        )
    return None


def r11(facts: dict[str, Any]) -> str | None:
    """Métastatique, âge < 75, ECOG 0-1, bilirubine normale → FOLFIRINOX."""
    if (
        facts.get("metastases")
        and (_num(facts.get("age")) or 0) < 75
        and facts.get("ecog") in (0, 1)
        and (_num(facts.get("bilirubine_ratio_lsn")) or 0) < 1.5
    ):
        return (
            "Maladie métastatique, bon état général, âge < 75 ans, bilirubine "
            "normale. Chimiothérapie de 1ère ligne par FOLFIRINOX ou mFOLFIRINOX. "
            "Options alternatives : gemcitabine + nab-paclitaxel, ou NALIRIFOX si accessibles."
        )
    return None


def r12(facts: dict[str, Any]) -> str | None:
    """Métastatique, ECOG 2 ou âge ≥ 75, bilirubine normale → gemcitabine."""
    if (
        facts.get("metastases")
        and (_num(facts.get("age")) or 0) >= 75
        and (_num(facts.get("bilirubine_ratio_lsn")) or 0) < 1.5
    ):
        return (
            "Maladie métastatique, âge ≥ 75 ans, bilirubine normale. Chimiothérapie "
            "de 1ère ligne par gemcitabine seule. Option : gemcitabine + "
            "nab-paclitaxel dans certains cas (à discuter en RCP)."
        )
    if (
        facts.get("metastases")
        and facts.get("ecog") == 2
        and (_num(facts.get("bilirubine_ratio_lsn")) or 0) < 1.5
    ):
        return (
            "Maladie métastatique, état général intermédiaire (ECOG 2), bilirubine "
            "normale. Chimiothérapie de 1ère ligne par gemcitabine seule. Option : "
            "gemcitabine + nab-paclitaxel dans certains cas (à discuter en RCP)."
        )
    return None


def r13(facts: dict[str, Any]) -> str | None:
    """Métastatique, bilirubine élevée → gemcitabine seule."""
    if (
        facts.get("metastases")
        and facts.get("ecog") in (0, 1, 2)
        and (_num(facts.get("bilirubine_ratio_lsn")) or 0) >= 1.5
    ):
        return (
            "Maladie métastatique, bilirubine élevée. Privilégier la gemcitabine "
            "seule en 1ère ligne, après évaluation d'un éventuel drainage biliaire "
            "si indiqué (voir T1)."
        )
    return None


def r14(facts: dict[str, Any]) -> str | None:
    """Métastatique, BRCA muté, sans progression ≥ 16 sem platine → olaparib."""
    if (
        facts.get("metastases")
        and facts.get("statut_brca") == "mute"
        and facts.get("pas_de_progression_apres_16_semaines_platine")
    ):
        return (
            "Maladie métastatique avec mutation germinale BRCA1/2, sans progression "
            "après ≥ 16 semaines de chimiothérapie à base de platine. Proposer "
            "olaparib en traitement de maintenance."
        )
    return None


# --- Situation « métastatique » — 2e et 3e ligne ------------------------

def r15(facts: dict[str, Any]) -> str | None:
    """2e ligne après gemcitabine, progression, ECOG 0-1 → 5-FU + nal-IRI."""
    if (
        facts.get("ligne_precedente") == "gemcitabine"
        and facts.get("reponse_traitement") == "progression"
        and facts.get("ecog") in (0, 1)
    ):
        return (
            "Progression après gemcitabine en 1ère ligne, bon état général. "
            "Chimiothérapie de 2ème ligne par 5-FU + nal-IRI (si accessible) ou "
            "5-FU + oxaliplatine."
        )
    return None


def r16(facts: dict[str, Any]) -> str | None:
    """2e ligne après FOLFIRINOX, progression, ECOG 0-1 → gemcitabine."""
    if (
        facts.get("ligne_precedente") == "FOLFIRINOX"
        and facts.get("reponse_traitement") == "progression"
        and facts.get("ecog") in (0, 1)
    ):
        return (
            "Progression après FOLFIRINOX en 1ère ligne, bon état général. "
            "Chimiothérapie de 2ème ligne par gemcitabine seule ou gemcitabine + "
            "paclitaxel si réponse tumorale nécessaire."
        )
    return None


def r17(facts: dict[str, Any]) -> str | None:
    """3ème ligne et au-delà, ECOG 0-1 → essai clinique + RCP moléculaire."""
    if (
        (_num(facts.get("ligne_traitement_actuelle")) or 0) >= 3
        and facts.get("ecog") in (0, 1)
    ):
        return (
            "Maladie métastatique en 3ème ligne ou au-delà, bon état général. "
            "Privilégier l'inclusion en essai clinique et la discussion en RCP "
            "moléculaire pour rechercher des anomalies actionnables."
        )
    return None


def r18(facts: dict[str, Any]) -> list[str]:
    """Thérapies ciblées et immunothérapie (conditions indépendantes)."""
    out: list[str] = []
    if facts.get("fusion_ntrk") == "positif":
        out.append(
            "Proposer larotrectinib (si aucune autre option standard, selon disponibilité et RCP)."
        )
    if facts.get("fusion_nrg1") == "positif":
        out.append(
            "Proposer zenocutuzumab, à discuter en RCP moléculaire (fusion NRG1)."
        )
    if facts.get("statut_kras") == "g12c":
        out.append(
            "Proposer adagrasib ou sotorasib, à discuter en RCP moléculaire (KRAS G12C, hors AMM)."
        )
    if facts.get("statut_msi_dmmr") == "positif":
        out.append(
            "Proposer une immunothérapie, à discuter en RCP moléculaire (statut MSI/dMMR positif)."
        )
    return out


# --- Règles transverses (tous stades) ----------------------------------

def t1(facts: dict[str, Any]) -> str | None:
    """Ictère + angiocholite et/ou bilirubine très élevée → drainage biliaire urgent."""
    if facts.get("ictere") and (
        facts.get("angiocholite")
        or (_num(facts.get("bilirubine")) or 0) > 250
    ):
        return (
            "Ictère avec angiocholite et/ou bilirubine très élevée. Proposer un "
            "drainage biliaire en urgence par CPRE (prothèse métallique courte), ou "
            "drainage sous échoendoscopie si échec CPRE et opérateur expérimenté."
        )
    return None


def t2(facts: dict[str, Any]) -> str | None:
    """Adénopathie à distance → contre-indication chirurgie première."""
    if facts.get("adenopathie_distance"):
        return (
            "Adénopathie à distance documentée (considérée comme métastase "
            "ganglionnaire). Contre-indication à une chirurgie première ; orienter "
            "vers une prise en charge médicale (chimiothérapie ± soins de support)."
        )
    return None


def t3(facts: dict[str, Any]) -> str | None:
    """Statut DPD et 5-FU / capécitabine."""
    if facts.get("statut_dpd") == "deficit_complet":
        return (
            "Déficit complet en DPD : contre-indication au 5-FU et à la capécitabine ; "
            "privilégier des schémas sans fluoropyrimidine."
        )
    if facts.get("statut_dpd") == "deficit_partiel":
        return (
            "Déficit partiel en DPD : ajustement de dose du 5-FU/capécitabine "
            "recommandé ; discuter en RCP."
        )
    return None


def t4(facts: dict[str, Any]) -> str | None:
    """Traitement médical prévu sans chirurgie d'emblée → preuve histologique."""
    if facts.get("traitement_medical_prevu") and not facts.get("chirurgie_d_emblee"):
        return (
            "Traitement médical prévu sans chirurgie d'emblée : obtenir une preuve "
            "histologique avant de débuter le traitement (exception : cas très "
            "particuliers après validation en RCP)."
        )
    return None


# --- Agrégation ---------------------------------------------------------

RULES: list[tuple[str, Callable[[dict[str, Any]], Any], str, str]] = [
    # (code, fonction, référence, grade)
    ("R01", r01, "TNCD 9.4.1.1 / 9.4.1.3", "A"),
    ("R02", r02, "TNCD 9.2.2.2 / 9.4.1.4", "accord_experts"),
    ("R03", r03, "TNCD 9.2.6.1 / 9.4.1.1", "accord_experts"),
    ("R04", r04, "TNCD 9.4.2.1", "B"),
    ("R05", r05, "TNCD 9.4.2.1", "accord_experts"),
    ("R06", r06, "TNCD 9.4.3.1", "A"),
    ("R07", r07, "TNCD 9.4.3.1", "A"),
    ("R08", r08, "TNCD 9.2.6.2 / 9.4.3", "accord_experts"),
    ("R09", r09, "TNCD 9.4.3.2 / 9.4.3.3", "B"),
    ("R10", r10, "TNCD 9.2.6.2 / 9.4.4", "accord_experts"),
    ("R11", r11, "TNCD 9.4.4.1", "A"),
    ("R12", r12, "TNCD 9.4.4.1", "A"),
    ("R13", r13, "TNCD 9.4.4.1", "A"),
    ("R14", r14, "TNCD 9.4.5", "B"),
    ("R15", r15, "TNCD 9.4.4.2", "A"),
    ("R16", r16, "TNCD 9.4.4.2", "B"),
    ("R17", r17, "TNCD 9.4.5", "accord_experts"),
    ("R18", r18, "TNCD 9.4.5", "B"),
    ("T1", t1, "TNCD 9.2.3.4", "A"),
    ("T2", t2, "TNCD 9.2.5 / 9.4.1.1", "accord_experts"),
    ("T3", t3, "TNCD 9.2.7.1", "A"),
    ("T4", t4, "TNCD 9.2.4 / 9.2.7.2", "A"),
]


def _flat_result(result: Any) -> list[dict[str, Any]]:
    """Normalise une conclusion (str unique ou liste pour R18) en liste de recommandations."""
    if isinstance(result, list):
        return result
    return [result] if result else []


def apply(facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Évalue toutes les règles dans l'ordre et retourne les recommandations matchées.

    Ne calcule pas la résécabilité : elle doit être fournie dans
    `facts["resecabilite"]` par l'appelant.
    """
    matched: list[dict[str, Any]] = []
    for code, fn, ref, grade in RULES:
        for conclusion in _flat_result(fn(facts)):
            matched.append({
                "code": code,
                "conclusion": conclusion,
                "reference": ref,
                "grade": grade,
            })
    return matched
