from datetime import date

from pydantic import BaseModel, ConfigDict


class TraitementCreate(BaseModel):
    id_protocole: int | None = None
    numero_ligne: int | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    reponse: str | None = None
    toxicite_residuelle: bool = False
    type_toxicite: str | None = None
    termine_comme_prevu: bool | None = None
    notes: str | None = None


class TraitementUpdate(BaseModel):
    id_protocole: int | None = None
    numero_ligne: int | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    reponse: str | None = None
    toxicite_residuelle: bool | None = None
    type_toxicite: str | None = None
    termine_comme_prevu: bool | None = None
    notes: str | None = None


class TraitementRead(TraitementCreate):
    model_config = ConfigDict(from_attributes=True)

    id_traitement: int
    id_dossier: int
