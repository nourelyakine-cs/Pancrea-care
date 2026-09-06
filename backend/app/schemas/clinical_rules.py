from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClinicalRulesCalculateRequest(BaseModel):
    categorie_t: str = Field(description="T1a, T1b, T1c, T2, T3 ou T4")
    categorie_n: str = Field(description="N0, N1 ou N2")
    categorie_m: str | None = Field(default=None, description="M0/M1; inféré de l'imagerie si absent")
    version_moteur: str = Field(default="tncd-2024-v1", max_length=20)


class DonneesDeriveesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_derive: int
    id_evaluation: int
    version_moteur: str
    source_code: str
    source_version: str
    date_calcul: datetime
    resecabilite: str | None
    categorie_t: str | None
    categorie_n: str | None
    categorie_m: str | None
    stade_global: str | None
    critere_abc_a: str | None
    critere_abc_b: bool | None
    critere_abc_c: bool | None
    sous_categorie_abc: str | None
    justification_calcul: str | None
