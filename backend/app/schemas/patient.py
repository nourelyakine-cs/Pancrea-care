from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientBase(BaseModel):
    nom: str
    prenom: str
    date_naissance: date | None = None
    sexe: str | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    date_naissance: date | None = None
    sexe: str | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None


class PatientRead(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id_patient: int
    date_creation: datetime
    date_modification: datetime
