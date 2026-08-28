import re
from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator


def validate_password_strength(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[^A-Za-z0-9]", v):
        raise ValueError("Password must contain at least one symbol")
    return v


class MedecinRegister(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    telephone: str | None = None
    specialite: str | None = None

    _validate_password = field_validator("password")(validate_password_strength)


class MedecinLogin(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str
    password_confirm: str

    _validate_password = field_validator("password")(validate_password_strength)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


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
