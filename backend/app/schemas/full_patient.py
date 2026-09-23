from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import Sexe
from app.schemas.dossier import AntecedentCreate, MutationCreate
from app.schemas.evaluation import (
    AnalyseCreate,
    BiologieCreate,
    ComorbiditeEvaluationCreate,
    EvaluationCreate,
    HistologieCreate,
    ImagerieCreate,
    MetastaseCreate,
)


class FullImagerieCreate(ImagerieCreate):
    metastases: list[MetastaseCreate] = []


class FullEvaluationCreate(EvaluationCreate):
    biologie: BiologieCreate | None = None
    imageries: list[FullImagerieCreate] = []
    histologie: HistologieCreate | None = None
    analyses: list[AnalyseCreate] = []
    comorbidites: list[ComorbiditeEvaluationCreate] = []


class FullPatientCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    # --- identité / dossier ---
    nom: str
    prenom: str
    date_naissance: date | None = None
    sexe: Sexe | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None

    # --- antécédents familiaux du dossier ---
    antecedents: list[AntecedentCreate] = []
    mutations: list[MutationCreate] = []

    # --- première évaluation clinique (toutes les données) ---
    evaluation: FullEvaluationCreate


class FullPatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_patient: int
    id_dossier: int
    id_evaluation: int
    id_decision: int
    date_creation: datetime
