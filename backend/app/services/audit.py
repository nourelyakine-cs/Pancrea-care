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
