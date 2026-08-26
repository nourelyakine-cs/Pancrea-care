from datetime import datetime

from pydantic import BaseModel


class MedecinRegister(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    telephone: str | None = None
    specialite: str | None = None


class MedecinLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MedecinResponse(BaseModel):
    id_medecin: int
    nom: str
    prenom: str
    email: str
    telephone: str | None
    specialite: str | None
    date_creation: datetime

    model_config = {"from_attributes": True}
