from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.reference import (
    Comorbidite,
    Gene,
    ProtocoleContexte,
    ProtocoleTraitement,
    SourceReferentiel,
)
from app.schemas.reference import (
    ComorbiditeCreate,
    ComorbiditeUpdate,
    GeneCreate,
    GeneUpdate,
    ProtocoleContexteCreate,
    ProtocoleCreate,
    ProtocoleUpdate,
    SourceCreate,
    SourceUpdate,
)
from app.services.audit import log_action


def _unique_conflict(label: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Un enregistrement de type '{label}' avec ce code existe déjà.",
    )


def _not_found(label: str, id_: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{label} {id_} introuvable.",
    )


# --- Gene ---------------------------------------------------------------------


def list_genes(db: Session, skip: int = 0, limit: int = 100) -> list[Gene]:
    return db.query(Gene).offset(skip).limit(limit).all()


def get_gene(db: Session, id_gene: int) -> Gene:
    obj = db.get(Gene, id_gene)
    if obj is None:
        raise _not_found("Gène", id_gene)
    return obj


def create_gene(db: Session, payload: GeneCreate, medecin_id: int | None = None) -> Gene:
    obj = Gene(**payload.model_dump())
    db.add(obj)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _unique_conflict("gène")
    log_action(db, medecin_id, "gene_create", "gene", obj.id_gene, payload.model_dump())
    db.commit()
    db.refresh(obj)
    return obj


def update_gene(db: Session, id_gene: int, payload: GeneUpdate, medecin_id: int | None = None) -> Gene:
    obj = get_gene(db, id_gene)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    log_action(db, medecin_id, "gene_update", "gene", obj.id_gene, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(obj)
    return obj


# --- Comorbidité ----------------------------------------------------------------


def list_comorbidites(db: Session, skip: int = 0, limit: int = 100) -> list[Comorbidite]:
    return db.query(Comorbidite).offset(skip).limit(limit).all()


def get_comorbidite(db: Session, id_comorbidite: int) -> Comorbidite:
    obj = db.get(Comorbidite, id_comorbidite)
    if obj is None:
        raise _not_found("Comorbidité", id_comorbidite)
    return obj


def create_comorbidite(db: Session, payload: ComorbiditeCreate, medecin_id: int | None = None) -> Comorbidite:
    obj = Comorbidite(**payload.model_dump())
    db.add(obj)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _unique_conflict("comorbidité")
    log_action(db, medecin_id, "comorbidite_create", "comorbidite", obj.id_comorbidite, payload.model_dump())
    db.commit()
    db.refresh(obj)
    return obj


def update_comorbidite(db: Session, id_comorbidite: int, payload: ComorbiditeUpdate, medecin_id: int | None = None) -> Comorbidite:
    obj = get_comorbidite(db, id_comorbidite)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    log_action(db, medecin_id, "comorbidite_update", "comorbidite", obj.id_comorbidite, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(obj)
    return obj


# --- Protocole -------------------------------------------------------------------


def list_protocoles(db: Session, skip: int = 0, limit: int = 100) -> list[ProtocoleTraitement]:
    return db.query(ProtocoleTraitement).offset(skip).limit(limit).all()


def get_protocole(db: Session, id_protocole: int) -> ProtocoleTraitement:
    obj = db.get(ProtocoleTraitement, id_protocole)
    if obj is None:
        raise _not_found("Protocole", id_protocole)
    return obj


def create_protocole(db: Session, payload: ProtocoleCreate, medecin_id: int | None = None) -> ProtocoleTraitement:
    obj = ProtocoleTraitement(**payload.model_dump())
    db.add(obj)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _unique_conflict("protocole")
    log_action(db, medecin_id, "protocole_create", "protocole_traitement", obj.id_protocole, payload.model_dump())
    db.commit()
    db.refresh(obj)
    return obj


def update_protocole(db: Session, id_protocole: int, payload: ProtocoleUpdate, medecin_id: int | None = None) -> ProtocoleTraitement:
    obj = get_protocole(db, id_protocole)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    log_action(db, medecin_id, "protocole_update", "protocole_traitement", obj.id_protocole, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(obj)
    return obj


def list_protocole_contextes(db: Session, id_protocole: int) -> list[ProtocoleContexte]:
    get_protocole(db, id_protocole)
    return db.query(ProtocoleContexte).filter(ProtocoleContexte.id_protocole == id_protocole).all()


def add_protocole_contexte(db: Session, id_protocole: int, payload: ProtocoleContexteCreate, medecin_id: int | None = None) -> ProtocoleContexte:
    get_protocole(db, id_protocole)
    obj = ProtocoleContexte(id_protocole=id_protocole, contexte_usage=payload.contexte_usage)
    db.add(obj)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _unique_conflict("contexte de protocole")
    log_action(db, medecin_id, "protocole_contexte_create", "protocole_contexte", None, payload.model_dump())
    db.commit()
    db.refresh(obj)
    return obj


def remove_protocole_contexte(db: Session, id_protocole: int, contexte_usage: str, medecin_id: int | None = None) -> None:
    obj = (
        db.query(ProtocoleContexte)
        .filter(
            ProtocoleContexte.id_protocole == id_protocole,
            ProtocoleContexte.contexte_usage == contexte_usage,
        )
        .first()
    )
    if obj is None:
        raise _not_found("Contexte de protocole", id_protocole)
    db.delete(obj)
    db.commit()


# --- Source référentiel --------------------------------------------------------------


def list_sources(db: Session, skip: int = 0, limit: int = 100) -> list[SourceReferentiel]:
    return db.query(SourceReferentiel).offset(skip).limit(limit).all()


def get_source(db: Session, id_source: int) -> SourceReferentiel:
    obj = db.get(SourceReferentiel, id_source)
    if obj is None:
        raise _not_found("Source", id_source)
    return obj


def create_source(db: Session, payload: SourceCreate, medecin_id: int | None = None) -> SourceReferentiel:
    obj = SourceReferentiel(**payload.model_dump())
    db.add(obj)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _unique_conflict("source")
    log_action(db, medecin_id, "source_create", "source_referentiel", obj.id_source, payload.model_dump())
    db.commit()
    db.refresh(obj)
    return obj


def update_source(db: Session, id_source: int, payload: SourceUpdate, medecin_id: int | None = None) -> SourceReferentiel:
    obj = get_source(db, id_source)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    log_action(db, medecin_id, "source_update", "source_referentiel", obj.id_source, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(obj)
    return obj
