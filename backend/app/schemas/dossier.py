from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import DegreParente, StatutDossier, StatutMutation


class DossierCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_medecin_referent: int | None = None
    statut: StatutDossier = "ouvert"


class DossierUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_medecin_referent: int | None = None
    statut: StatutDossier | None = None


class DossierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_dossier: int
    id_patient: int
    id_medecin_referent: int | None = None
    date_creation: datetime
    date_modification: datetime
    statut: StatutDossier


class AntecedentCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    degre_parente: DegreParente = "inconnu"
    nombre_apparentes: int = 1
    type_cancer: str = "pancreas"


class AntecedentUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    degre_parente: DegreParente | None = None
    nombre_apparentes: int | None = None
    type_cancer: str | None = None


class AntecedentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_antecedent: int
    id_dossier: int
    degre_parente: DegreParente | None = None
    nombre_apparentes: int | None = None
    type_cancer: str | None = None


class MutationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_gene: int
    statut: StatutMutation = "mute"
    date_test: datetime | None = None


class MutationUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    statut: StatutMutation | None = None
    date_test: datetime | None = None


class MutationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_mutation: int
    id_dossier: int
    id_gene: int
    statut: StatutMutation | None = None
    date_test: datetime | None = None