from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_journal: int
    id_medecin: int | None = None
    action: str | None = None
    type_entite: str | None = None
    id_entite: int | None = None
    detail: dict[str, Any] | None = None
    date_action: datetime
