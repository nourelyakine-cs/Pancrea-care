from sqlalchemy.orm import Session

from app.models.audit import JournalAudit


def log_action(
    db: Session,
    medecin_id: int | None,
    action: str,
    type_entite: str,
    id_entite: int | None = None,
    detail: dict | None = None,
) -> JournalAudit:
    entry = JournalAudit(
        id_medecin=medecin_id,
        action=action,
        type_entite=type_entite,
        id_entite=id_entite,
        detail=detail,
    )
    db.add(entry)
    return entry


def list_audit(
    db: Session,
    medecin_id: int | None = None,
    type_entite: str | None = None,
    id_entite: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[JournalAudit]:
    query = db.query(JournalAudit)
    if medecin_id:
        query = query.filter(JournalAudit.id_medecin == medecin_id)
    if type_entite:
        query = query.filter(JournalAudit.type_entite == type_entite)
    if id_entite:
        query = query.filter(JournalAudit.id_entite == id_entite)
    return query.order_by(JournalAudit.date_action.desc()).offset(skip).limit(limit).all()
