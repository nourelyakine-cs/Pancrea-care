"""Cloisonnement des données par médecin référent.

Règle unique appliquée partout : un médecin n'accède qu'aux dossiers dont il est
le référent (`dossier_patient.id_medecin_referent`). Les dossiers dont
`id_medecin_referent` est NULL sont considérés comme des données historiques
(importées ou créées avant le cloisonnement) : ils restent lisibles par tous,
faute d'information de propriété. Un patient sans aucun dossier est traité de la
même façon.

Les refus renvoient 404 et non 403 : un 403 confirmerait au médecin qu'un
patient existe chez quelqu'un d'autre, ce qui suffirait à énumérer le reste des
dossiers de la plateforme.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.dossier import DossierPatient
from app.models.evaluation import EvaluationClinique
from app.models.patient import Patient


def _dossiers_visibles(db: Session, medecin_id: int | None):
    """Sous-requête des `id_patient` accessibles au médecin connecté."""
    return (
        db.query(DossierPatient.id_patient)
        .filter(
            (DossierPatient.id_medecin_referent == medecin_id)
            | (DossierPatient.id_medecin_referent.is_(None))
        )
    )


def patients_visibles(db: Session, medecin_id: int | None):
    """Query `Patient` restreinte aux patients accessibles au médecin.

    `medecin_id is None` (mode démo / appel interne sans contexte d'authentification)
    ne restreint rien.
    """
    query = db.query(Patient)
    if medecin_id is None:
        return query
    sans_dossier = ~Patient.id_patient.in_(db.query(DossierPatient.id_patient))
    return query.filter(
        Patient.id_patient.in_(_dossiers_visibles(db, medecin_id)) | sans_dossier
    )


def patient_accessible(db: Session, id_patient: int, medecin_id: int | None) -> bool:
    if medecin_id is None:
        return True
    referents = [
        row[0]
        for row in db.query(DossierPatient.id_medecin_referent)
        .filter(DossierPatient.id_patient == id_patient)
        .all()
    ]
    if not referents:
        # Aucun dossier : aucune information de propriété (donnée historique).
        return True
    return any(referent is None or referent == medecin_id for referent in referents)


def dossier_accessible(db: Session, id_dossier: int, medecin_id: int | None) -> bool:
    if medecin_id is None:
        return True
    dossier = db.get(DossierPatient, id_dossier)
    if dossier is None:
        return False
    return (
        dossier.id_medecin_referent is None
        or dossier.id_medecin_referent == medecin_id
    )


def evaluation_accessible(db: Session, id_evaluation: int, medecin_id: int | None) -> bool:
    if medecin_id is None:
        return True
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None:
        return False
    return dossier_accessible(db, evaluation.id_dossier, medecin_id)


def exiger_patient(db: Session, id_patient: int, medecin_id: int | None) -> Patient:
    patient = db.get(Patient, id_patient)
    if patient is None or not patient_accessible(db, id_patient, medecin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {id_patient} introuvable.",
        )
    return patient


def exiger_dossier(db: Session, id_dossier: int, medecin_id: int | None) -> DossierPatient:
    dossier = db.get(DossierPatient, id_dossier)
    if dossier is None or not dossier_accessible(db, id_dossier, medecin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable.",
        )
    return dossier


def exiger_evaluation(db: Session, id_evaluation: int, medecin_id: int | None) -> EvaluationClinique:
    evaluation = db.get(EvaluationClinique, id_evaluation)
    if evaluation is None or not evaluation_accessible(db, id_evaluation, medecin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Évaluation {id_evaluation} introuvable.",
        )
    return evaluation