from datetime import date

from pydantic import BaseModel, ConfigDict


# --- Gene ---------------------------------------------------------------------


class GeneCreate(BaseModel):
    code: str
    libelle: str | None = None
    syndrome: str | None = None
    cancers_associes: str | None = None


class GeneUpdate(BaseModel):
    code: str | None = None
    libelle: str | None = None
    syndrome: str | None = None
    cancers_associes: str | None = None


class GeneRead(GeneCreate):
    model_config = ConfigDict(from_attributes=True)

    id_gene: int


# --- Comorbidite ---------------------------------------------------------------


class ComorbiditeCreate(BaseModel):
    code: str
    libelle_fr: str | None = None
    libelle_en: str | None = None


class ComorbiditeUpdate(BaseModel):
    code: str | None = None
    libelle_fr: str | None = None
    libelle_en: str | None = None


class ComorbiditeRead(ComorbiditeCreate):
    model_config = ConfigDict(from_attributes=True)

    id_comorbidite: int


# --- Protocole ------------------------------------------------------------------


class ProtocoleCreate(BaseModel):
    code: str
    libelle_fr: str | None = None
    libelle_en: str | None = None
    description: str | None = None


class ProtocoleUpdate(BaseModel):
    code: str | None = None
    libelle_fr: str | None = None
    libelle_en: str | None = None
    description: str | None = None


class ProtocoleRead(ProtocoleCreate):
    model_config = ConfigDict(from_attributes=True)

    id_protocole: int


class ProtocoleContexteCreate(BaseModel):
    contexte_usage: str


class ProtocoleContexteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_protocole: int
    contexte_usage: str


# --- Source référentiel -----------------------------------------------------------


class SourceCreate(BaseModel):
    code: str
    titre: str | None = None
    version: str | None = None
    date_publication: date | None = None


class SourceUpdate(BaseModel):
    code: str | None = None
    titre: str | None = None
    version: str | None = None
    date_publication: date | None = None


class SourceRead(SourceCreate):
    model_config = ConfigDict(from_attributes=True)

    id_source: int
