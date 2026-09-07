from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.dossier import DossierPatient
from app.models.evaluation import (
    Biologie,
    EvaluationClinique,
    EvaluationComorbidite,
    HistologieBiologie,
    Imagerie,
)
from app.models.patient import Patient
from app.models.traitement import Traitement


def _age(date_naissance: date | None, reference: date | None) -> int | None:
    if date_naissance is None or reference is None:
        return None
    value = reference.year - date_naissance.year
    if (reference.month, reference.day) < (date_naissance.month, date_naissance.day):
        value -= 1
    return value


def _comorbidites_lourdes(db: Session, id_evaluation: int) -> bool:
    return (
        db.query(EvaluationComorbidite)
        .filter(
            EvaluationComorbidite.id_evaluation == id_evaluation,
            EvaluationComorbidite.severite == "majeure",
        )
        .first()
        is not None
    )


def _patient_non_operable(
    comorbidites_lourdes: bool,
    etat_nutritionnel: str | None,
    ecog: int | None,
) -> bool | None:
    etat_severe = etat_nutritionnel == "denutrition_severe"
    etat_connu = etat_nutritionnel is not None and etat_nutritionnel != "inconnu"
    ecog_severe = ecog is not None and ecog >= 3
    if comorbidites_lourdes or etat_severe or ecog_severe:
        return True
    if etat_connu and ecog is not None:
        return False
    return None


def _normalise_protocole(code: str | None) -> str | None:
    if not code:
        return None
    value = code.strip().lower().replace("-", "").replace("_", "")
    aliases = {
        "mfolfirinox": "folfirinox",
        "folfirinox": "folfirinox",
        "gemcitabine": "gemcitabine",
        "gemcitabin": "gemcitabine",
        "gemcitabine+nabpaclitaxel": "gemcitabine_nab_paclitaxel",
        "gemcap": "gemcitabine",
    }
    return aliases.get(value, value)


def _treatment_facts(db: Session, id_dossier: int) -> dict[str, Any]:
    treatments = (
        db.query(Traitement)
        .filter(Traitement.id_dossier == id_dossier)
        .order_by(Traitement.numero_ligne.asc(), Traitement.date_debut.asc(), Traitement.id_traitement.asc())
        .all()
    )
    if not treatments:
        return {
            "ligne_traitement_actuelle": None,
            "ligne_precedente": None,
            "reponse_traitement": None,
            "duree_chimiotherapie_mois": None,
            "toxicite_residuelle": None,
        }

    with_line = [item for item in treatments if item.numero_ligne is not None]
    current_line = max((item.numero_ligne for item in with_line), default=None)
    current = next(
        (item for item in reversed(with_line) if item.numero_ligne == current_line),
        None,
    )
    previous = None
    if current_line is not None:
        previous = next(
            (item for item in reversed(with_line) if item.numero_ligne is not None and item.numero_ligne < current_line),
            None,
        )

    start = current.date_debut if current else None
    end = (current.date_fin if current and current.date_fin else date.today()) if current else None
    duration = None
    if start and end and end >= start:
        duration = round((end - start).days / 30.4375, 2)

    return {
        "ligne_traitement_actuelle": current_line,
        "ligne_precedente": _normalise_protocole(previous.protocole.code if previous and previous.protocole else None),
        "reponse_traitement": current.reponse if current else None,
        "duree_chimiotherapie_mois": duration,
        "toxicite_residuelle": current.toxicite_residuelle if current else None,
    }


def build_rule_facts(
    db: Session,
    evaluation: EvaluationClinique,
    derived: DonneesDerivees,
    biology: Biologie | None,
    image: Imagerie,
    histology: HistologieBiologie | None = None,
) -> dict[str, Any]:
    dossier = db.get(DossierPatient, evaluation.id_dossier)
    patient = db.get(Patient, dossier.id_patient) if dossier else None
    treatment = _treatment_facts(db, evaluation.id_dossier)
    return {
        "resecabilite": derived.resecabilite,
        "stade_global": derived.stade_global,
        "categorie_t": derived.categorie_t,
        "categorie_n": derived.categorie_n,
        "categorie_m": derived.categorie_m,
        "critere_abc_b": derived.critere_abc_b,
        "critere_abc_c": derived.critere_abc_c,
        "type_abc": derived.sous_categorie_abc,
        "metastases": image.metastases_presentes,
        "adenopathie_distance": image.extension_ganglionnaire_distance,
        "ecog": evaluation.ecog,
        "ictere": evaluation.ictere,
        "ca19_9": float(biology.ca19_9) if biology and biology.ca19_9 is not None else None,
        "cholestase": biology.cholestase if biology else None,
        "bilirubine": float(biology.bilirubine) if biology and biology.bilirubine is not None else None,
        "bilirubine_ratio_lsn": float(biology.bilirubine_ratio_lsn) if biology and biology.bilirubine_ratio_lsn is not None else None,
        "statut_dpd": biology.statut_dpd if biology else None,
        "age": _age(patient.date_naissance if patient else None, evaluation.date_evaluation),
        "statut_brca": histology.statut_brca_germinal if histology else None,
        "statut_kras": histology.statut_kras if histology else None,
        "statut_msi_dmmr": histology.statut_msi_dmmr if histology else None,
        "fusion_ntrk": histology.fusion_ntrk if histology else None,
        "fusion_nrg1": histology.fusion_nrg1 if histology else None,
        "preuve_histologique": histology.preuve_histologique if histology else None,
        "patient_non_operable": _patient_non_operable(
            _comorbidites_lourdes(db, evaluation.id_evaluation),
            evaluation.etat_nutritionnel,
            evaluation.ecog,
        ),
        # Ces champs nécessitent la migration parcours_therapeutique_clinique.
        "tumeur_controlee": None,
        "nouvelles_metastases": None,
        "traitement_medical_prevu": None,
        "chirurgie_d_emblee": None,
        "angiocholite": None,
        "pas_de_progression_apres_16_semaines_platine": None,
        **treatment,
    }
