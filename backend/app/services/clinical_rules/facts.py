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


def _age(date_naissance: date | None, reference: date | None) -> int | None:
    if date_naissance is None or reference is None:
        return None
    value = reference.year - date_naissance.year
    if (reference.month, reference.day) < (date_naissance.month, date_naissance.day):
        value -= 1
    return value


def _comorbidites_lourdes(db: Session, id_evaluation: int) -> bool:
    """Vrai si au moins une comorbidité de sévérité 'majeure' est liée à l'évaluation.

    Contrairement à l'ECOG ou à l'état nutritionnel, il n'existe pas de valeur
    « inconnu » explicite pour ce critère (une évaluation sans ligne dans
    `evaluation_comorbidite` est considérée comme sans comorbidité majeure
    connue) : ce sous-critère est donc toujours résolu en True/False, jamais None.
    """
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
    """R03 : patient jugé non opérable si comorbidités lourdes, dénutrition
    sévère et/ou ECOG >= 3 (un seul critère positif suffit).

    - True dès qu'un des trois critères est positif, peu importe les autres.
    - False seulement si les trois critères sont connus et négatifs.
    - None (inconnu) si aucun critère n'est positif mais que l'ECOG et/ou
      l'état nutritionnel ne sont pas renseignés : conformément au reste du
      moteur (cf. cholestase, statut_dpd...), une donnée manquante ne doit
      jamais être interprétée comme négative.
    """
    etat_severe = etat_nutritionnel == "denutrition_severe"
    etat_connu = etat_nutritionnel is not None and etat_nutritionnel != "inconnu"
    ecog_severe = ecog is not None and ecog >= 3

    if comorbidites_lourdes or etat_severe or ecog_severe:
        return True
    if etat_connu and ecog is not None:
        return False
    return None


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
    return {
        # Calculated clinical classification
        "resecabilite": derived.resecabilite,
        "stade_global": derived.stade_global,
        "categorie_t": derived.categorie_t,
        "categorie_n": derived.categorie_n,
        "categorie_m": derived.categorie_m,
        # Imaging: preserve NULL as unknown
        "metastases": image.metastases_presentes,
        "adenopathie_distance": image.extension_ganglionnaire_distance,
        # Clinical evaluation
        "ecog": evaluation.ecog,
        "ictere": evaluation.ictere,
        # Biology
        "ca19_9": float(biology.ca19_9) if biology and biology.ca19_9 is not None else None,
        "cholestase": biology.cholestase if biology else None,
        "bilirubine": float(biology.bilirubine) if biology and biology.bilirubine is not None else None,
        "bilirubine_ratio_lsn": (
            float(biology.bilirubine_ratio_lsn)
            if biology and biology.bilirubine_ratio_lsn is not None
            else None
        ),
        "statut_dpd": biology.statut_dpd if biology else None,
        # Patient and molecular data
        "age": _age(patient.date_naissance if patient else None, evaluation.date_evaluation),
        "statut_brca": histology.statut_brca_germinal if histology else None,
        "statut_kras": histology.statut_kras if histology else None,
        "statut_msi_dmmr": histology.statut_msi_dmmr if histology else None,
        "fusion_ntrk": histology.fusion_ntrk if histology else None,
        "fusion_nrg1": histology.fusion_nrg1 if histology else None,
        # R03 : comorbidités lourdes (sévérité 'majeure') OU dénutrition sévère OU ECOG >= 3.
        "patient_non_operable": _patient_non_operable(
            _comorbidites_lourdes(db, evaluation.id_evaluation),
            evaluation.etat_nutritionnel,
            evaluation.ecog,
        ),
        # Not represented by current input tables: intentionally unknown.
        "tumeur_controlee": None,
        "nouvelles_metastases": None,
        "duree_chimiotherapie_mois": None,
        "traitement_medical_prevu": None,
        "chirurgie_d_emblee": None,
        "angiocholite": None,
        "pas_de_progression_apres_16_semaines_platine": None,
        "ligne_precedente": None,
        "reponse_traitement": None,
        "ligne_traitement_actuelle": None,
    }
