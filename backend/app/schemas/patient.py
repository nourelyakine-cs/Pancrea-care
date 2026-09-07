from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import Sexe


class PatientBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    nom: str
    prenom: str
    date_naissance: date | None = None
    sexe: Sexe | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    nom: str | None = None
    prenom: str | None = None
    date_naissance: date | None = None
    sexe: Sexe | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None


class PatientRead(PatientBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_patient: int
    date_creation: datetime
    date_modification: datetime