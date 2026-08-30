from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.dossier import DossierPatient
from app.models.traitement import Traitement
from app.schemas.traitement import TraitementCreate, TraitementUpdate
from app.services.audit import log_action


def create_traitement(
    db: Session,
    id_dossier: int,
    payload: TraitementCreate,
    medecin_id: int | None = None,
) -> Traitement:
    dossier = db.get(DossierPatient, id_dossier)
    if dossier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable, impossible d'enregistrer un traitement.",
        )
    traitement = Traitement(id_dossier=id_dossier, **payload.model_dump())
    db.add(traitement)
    db.flush()
    log_action(
        db,
        medecin_id=medecin_id,
        action="traitement_create",
        type_entite="traitement",
        id_entite=traitement.id_traitement,
        detail={"id_dossier": id_dossier, **payload.model_dump()},
    )
    db.commit()
    db.refresh(traitement)
    return traitement


def list_traitements(db: Session, id_dossier: int) -> list[Traitement]:
    dossier = db.get(DossierPatient, id_dossier)
    if dossier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable.",
        )
    return (
        db.query(Traitement)
        .filter(Traitement.id_dossier == id_dossier)
        .order_by(Traitement.numero_ligne.asc())
        .all()
    )


def get_traitement(db: Session, id_traitement: int) -> Traitement:
    traitement = db.get(Traitement, id_traitement)
    if traitement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Traitement {id_traitement} introuvable.",
        )
    return traitement


def update_traitement(
    db: Session,
    id_traitement: int,
    payload: TraitementUpdate,
    medecin_id: int | None = None,
) -> Traitement:
    traitement = get_traitement(db, id_traitement)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(traitement, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="traitement_update",
        type_entite="traitement",
        id_entite=traitement.id_traitement,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(traitement)
    return traitement


def delete_traitement(
    db: Session,
    id_traitement: int,
    medecin_id: int | None = None,
) -> None:
    traitement = get_traitement(db, id_traitement)
    log_action(
        db,
        medecin_id=medecin_id,
        action="traitement_delete",
        type_entite="traitement",
        id_entite=traitement.id_traitement,
    )
    db.delete(traitement)
    db.commit()
