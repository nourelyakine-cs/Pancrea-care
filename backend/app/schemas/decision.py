from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_decision: int
    id_evaluation: int
    date_decision: datetime
    decide_par: int | None = None
    source_code: str | None = None
    source_version: str | None = None
    snapshot_patient: dict[str, Any] | None = None
    resume: str | None = None
    necessite_rcp: bool | None = None


class DecisionDetailRead(DecisionRead):
    pass
