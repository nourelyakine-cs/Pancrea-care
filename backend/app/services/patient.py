from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.dossier import DossierPatient
from app.models.evaluation import EvaluationClinique
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.audit import log_action


def create_patient(
    db: Session,
    payload: PatientCreate,
    medecin_id: int | None = None,
) -> Patient:
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.flush()
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_create",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail=payload.model_dump(),
    )
    db.commit()
    db.refresh(patient)
    return patient


def list_patients(
    db: Session,
    nom: str | None = None,
    sexe: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Patient]:
    query = db.query(Patient)
    if nom:
        query = query.filter(Patient.nom.ilike(f"%{nom}%"))
    if sexe:
        query = query.filter(Patient.sexe == sexe)
    patients = query.offset(skip).limit(limit).all()
    _attach_dernier_bilan(db, patients)
    return patients


def _attach_dernier_bilan(db: Session, patients: list[Patient]) -> None:
    """Attache à chaque patient son dossier, sa dernière évaluation et le
    dernier bilan calculé (stade global + catégories TNM)."""
    patient_ids = [p.id_patient for p in patients]
    if not patient_ids:
        return

    dossiers = (
        db.query(DossierPatient)
        .filter(DossierPatient.id_patient.in_(patient_ids))
        .order_by(DossierPatient.id_dossier.asc())
        .all()
    )
    if not dossiers:
        return

    evaluations = (
        db.query(EvaluationClinique)
        .filter(
            EvaluationClinique.id_dossier.in_(
                [d.id_dossier for d in dossiers]
            )
        )
        .order_by(
            EvaluationClinique.date_evaluation.desc(),
            EvaluationClinique.id_evaluation.desc(),
        )
        .all()
    )

    derniere_eval: dict[int, EvaluationClinique] = {}
    for evaluation in evaluations:
        derniere_eval.setdefault(evaluation.id_dossier, evaluation)

    derniers_derivees: dict[int, DonneesDerivees] = {}
    if evaluations:
        derivees = (
            db.query(DonneesDerivees)
            .filter(
                DonneesDerivees.id_evaluation.in_(
                    [e.id_evaluation for e in evaluations]
                )
            )
            .all()
        )
        for derivee in derivees:
            courant = derniers_derivees.get(derivee.id_evaluation)
            if courant is None or derivee.date_calcul > courant.date_calcul:
                derniers_derivees[derivee.id_evaluation] = derivee

    dossier_par_patient: dict[int, DossierPatient] = {}
    for dossier in dossiers:
        dossier_par_patient.setdefault(dossier.id_patient, dossier)

    for patient in patients:
        dossier = dossier_par_patient.get(patient.id_patient)
        if dossier is None:
            continue
        evaluation = derniere_eval.get(dossier.id_dossier)
        derivee = (
            derniers_derivees.get(evaluation.id_evaluation)
            if evaluation
            else None
        )
        patient.id_dossier = dossier.id_dossier
        patient.id_evaluation = (
            evaluation.id_evaluation if evaluation else None
        )
        patient.date_derniere_evaluation = (
            evaluation.date_evaluation if evaluation else None
        )
        patient.stade_global = derivee.stade_global if derivee else None
        patient.resecabilite = derivee.resecabilite if derivee else None
        patient.categorie_t = derivee.categorie_t if derivee else None
        patient.categorie_n = derivee.categorie_n if derivee else None
        patient.categorie_m = derivee.categorie_m if derivee else None


def get_patient(db: Session, id_patient: int) -> Patient:
    patient = db.get(Patient, id_patient)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


def update_patient(
    db: Session,
    id_patient: int,
    payload: PatientUpdate,
    medecin_id: int | None = None,
) -> Patient:
    patient = get_patient(db, id_patient)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_update",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(
    db: Session,
    id_patient: int,
    medecin_id: int | None = None,
) -> None:
    patient = get_patient(db, id_patient)
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_delete",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail={"nom": patient.nom, "prenom": patient.prenom},
    )
    try:
        db.delete(patient)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Impossible de supprimer ce patient : un dossier clinique lui est "
                "associé. Pour respecter la traçabilité médico-légale, clôturez ou "
                "archivez le dossier (statut 'clos'/'archive') au lieu de supprimer "
                "le patient."
            ),
        )
