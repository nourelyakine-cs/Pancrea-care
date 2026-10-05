from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import DegreParente, StatutMutation


class AntecedentCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    degre_parente: DegreParente = "inconnu"
    nombre_apparentes: int = 1
    type_cancer: str = "pancreas"


class MutationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_gene: int
    statut: StatutMutation = "mute"
    date_test: datetime | None = None
