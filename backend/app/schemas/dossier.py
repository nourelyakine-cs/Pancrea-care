from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DossierCreate(BaseModel):
    id_medecin_referent: int | None = None
    statut: str = "ouvert"


class DossierUpdate(BaseModel):
    id_medecin_referent: int | None = None
    statut: str | None = None


class DossierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_dossier: int
    id_patient: int
    id_medecin_referent: int | None = None
    date_creation: datetime
    date_modification: datetime
    statut: str


class AntecedentCreate(BaseModel):
    degre_parente: str = "inconnu"
    nombre_apparentes: int = 1
    type_cancer: str = "pancreas"


class AntecedentUpdate(BaseModel):
    degre_parente: str | None = None
    nombre_apparentes: int | None = None
    type_cancer: str | None = None


class AntecedentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_antecedent: int
    id_dossier: int
    degre_parente: str | None = None
    nombre_apparentes: int | None = None
    type_cancer: str | None = None


class MutationCreate(BaseModel):
    id_gene: int
    statut: str = "mute"
    date_test: datetime | None = None


class MutationUpdate(BaseModel):
    statut: str | None = None
    date_test: datetime | None = None


class MutationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_mutation: int
    id_dossier: int
    id_gene: int
    statut: str | None = None
    date_test: datetime | None = None
