from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.dossier import AntecedentFamilial, DossierPatient, MutationGerminale
from app.models.patient import Patient
from app.schemas.dossier import (
    AntecedentCreate,
    AntecedentUpdate,
    DossierCreate,
    DossierUpdate,
    MutationCreate,
    MutationUpdate,
)
from app.services.audit import log_action


def create_dossier(
    db: Session,
    id_patient: int,
    payload: DossierCreate,
    medecin_id: int | None = None,
) -> DossierPatient:
    patient = db.get(Patient, id_patient)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient {id_patient} introuvable, impossible d'ouvrir un dossier.",
        )
    dossier = DossierPatient(id_patient=id_patient, **payload.model_dump())
    db.add(dossier)
    db.flush()
    log_action(
        db,
        medecin_id=medecin_id,
        action="dossier_create",
        type_entite="dossier_patient",
        id_entite=dossier.id_dossier,
        detail={"id_patient": id_patient, **payload.model_dump()},
    )
    db.commit()
    db.refresh(dossier)
    return dossier


def list_dossiers(
    db: Session,
    statut: str | None = None,
    id_patient: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[DossierPatient]:
    query = db.query(DossierPatient)
    if statut:
        query = query.filter(DossierPatient.statut == statut)
    if id_patient:
        query = query.filter(DossierPatient.id_patient == id_patient)
    return query.offset(skip).limit(limit).all()


def get_dossier(db: Session, id_dossier: int) -> DossierPatient:
    dossier = db.get(DossierPatient, id_dossier)
    if dossier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable.",
        )
    return dossier


def update_dossier(
    db: Session,
    id_dossier: int,
    payload: DossierUpdate,
    medecin_id: int | None = None,
) -> DossierPatient:
    dossier = get_dossier(db, id_dossier)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(dossier, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="dossier_update",
        type_entite="dossier_patient",
        id_entite=dossier.id_dossier,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(dossier)
    return dossier


def set_dossier_statut(
    db: Session,
    id_dossier: int,
    statut: str,
    medecin_id: int | None = None,
) -> DossierPatient:
    return update_dossier(
        db, id_dossier, DossierUpdate(statut=statut), medecin_id=medecin_id
    )


# --- Antécédents familiaux --------------------------------------------------


def list_antecedents(db: Session, id_dossier: int) -> list[AntecedentFamilial]:
    get_dossier(db, id_dossier)
    return db.query(AntecedentFamilial).filter(AntecedentFamilial.id_dossier == id_dossier).all()


def create_antecedent(
    db: Session,
    id_dossier: int,
    payload: AntecedentCreate,
    medecin_id: int | None = None,
) -> AntecedentFamilial:
    get_dossier(db, id_dossier)
    antecedent = AntecedentFamilial(id_dossier=id_dossier, **payload.model_dump())
    db.add(antecedent)
    db.flush()
    log_action(
        db,
        medecin_id=medecin_id,
        action="antecedent_create",
        type_entite="antecedent_familial",
        id_entite=antecedent.id_antecedent,
        detail=payload.model_dump(),
    )
    db.commit()
    db.refresh(antecedent)
    return antecedent


def get_antecedent(db: Session, id_antecedent: int) -> AntecedentFamilial:
    antecedent = db.get(AntecedentFamilial, id_antecedent)
    if antecedent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Antécédent {id_antecedent} introuvable.",
        )
    return antecedent


def update_antecedent(
    db: Session,
    id_antecedent: int,
    payload: AntecedentUpdate,
    medecin_id: int | None = None,
) -> AntecedentFamilial:
    antecedent = get_antecedent(db, id_antecedent)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(antecedent, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="antecedent_update",
        type_entite="antecedent_familial",
        id_entite=antecedent.id_antecedent,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(antecedent)
    return antecedent


def delete_antecedent(
    db: Session,
    id_antecedent: int,
    medecin_id: int | None = None,
) -> None:
    antecedent = get_antecedent(db, id_antecedent)
    log_action(
        db,
        medecin_id=medecin_id,
        action="antecedent_delete",
        type_entite="antecedent_familial",
        id_entite=antecedent.id_antecedent,
    )
    db.delete(antecedent)
    db.commit()


# --- Mutations germinales ---------------------------------------------------


def list_mutations(db: Session, id_dossier: int) -> list[MutationGerminale]:
    get_dossier(db, id_dossier)
    return db.query(MutationGerminale).filter(MutationGerminale.id_dossier == id_dossier).all()


def create_mutation(
    db: Session,
    id_dossier: int,
    payload: MutationCreate,
    medecin_id: int | None = None,
) -> MutationGerminale:
    get_dossier(db, id_dossier)
    mutation = MutationGerminale(id_dossier=id_dossier, **payload.model_dump())
    db.add(mutation)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Le gène {payload.id_gene} est déjà testé pour ce dossier (contrainte unique dossier+gene).",
        )
    log_action(
        db,
        medecin_id=medecin_id,
        action="mutation_create",
        type_entite="mutation_germinale",
        id_entite=mutation.id_mutation,
        detail=payload.model_dump(),
    )
    db.commit()
    db.refresh(mutation)
    return mutation


def get_mutation(db: Session, id_mutation: int) -> MutationGerminale:
    mutation = db.get(MutationGerminale, id_mutation)
    if mutation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mutation {id_mutation} introuvable.",
        )
    return mutation


def update_mutation(
    db: Session,
    id_mutation: int,
    payload: MutationUpdate,
    medecin_id: int | None = None,
) -> MutationGerminale:
    mutation = get_mutation(db, id_mutation)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(mutation, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="mutation_update",
        type_entite="mutation_germinale",
        id_entite=mutation.id_mutation,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(mutation)
    return mutation


def delete_mutation(
    db: Session,
    id_mutation: int,
    medecin_id: int | None = None,
) -> None:
    mutation = get_mutation(db, id_mutation)
    log_action(
        db,
        medecin_id=medecin_id,
        action="mutation_delete",
        type_entite="mutation_germinale",
        id_entite=mutation.id_mutation,
    )
    db.delete(mutation)
    db.commit()
