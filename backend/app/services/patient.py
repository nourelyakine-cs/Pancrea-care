from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
    return query.offset(skip).limit(limit).all()


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
