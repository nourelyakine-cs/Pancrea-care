from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


# --- Évaluation clinique ----------------------------------------------------


class EvaluationCreate(BaseModel):
    date_evaluation: date
    contexte: str = "diagnostic"
    ecog: int | None = None
    etat_nutritionnel: str = "inconnu"
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: str = "inconnu"


class EvaluationUpdate(BaseModel):
    date_evaluation: date | None = None
    contexte: str | None = None
    ecog: int | None = None
    etat_nutritionnel: str | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: str | None = None


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_evaluation: int
    id_dossier: int
    id_medecin_evaluateur: int | None = None
    date_evaluation: date
    contexte: str | None = None
    ecog: int | None = None
    etat_nutritionnel: str | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: str | None = None
    date_creation: datetime


# --- Biologie ----------------------------------------------------------------


class BiologieCreate(BaseModel):
    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: str = "inconnu"
    statut_dpd: str = "non_teste"
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieUpdate(BaseModel):
    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: str | None = None
    statut_dpd: str | None = None
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieRead(BiologieCreate):
    model_config = ConfigDict(from_attributes=True)

    id_biologie: int
    id_evaluation: int


# --- Imagerie ----------------------------------------------------------------


class ImagerieCreate(BaseModel):
    type_imagerie: str
    date_imagerie: date
    localisation_tumorale: str = "inconnu"
    taille_tumorale_cm: Decimal | None = None
    contact_ams: str | None = None
    contact_tronc_coeliaque: str | None = None
    contact_art_hepatique: str | None = None
    contact_vms_vp: str | None = None
    extension_ganglionnaire_regionale: bool = False
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None


class ImagerieUpdate(BaseModel):
    type_imagerie: str | None = None
    date_imagerie: date | None = None
    localisation_tumorale: str | None = None
    taille_tumorale_cm: Decimal | None = None
    contact_ams: str | None = None
    contact_tronc_coeliaque: str | None = None
    contact_art_hepatique: str | None = None
    contact_vms_vp: str | None = None
    extension_ganglionnaire_regionale: bool | None = None
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None


class ImagerieRead(ImagerieCreate):
    model_config = ConfigDict(from_attributes=True)

    id_imagerie: int
    id_evaluation: int


# --- Métastase ---------------------------------------------------------------


class MetastaseCreate(BaseModel):
    site: str
    detail: str | None = None


class MetastaseUpdate(BaseModel):
    site: str | None = None
    detail: str | None = None


class MetastaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_metastase: int
    id_imagerie: int
    site: str | None = None
    detail: str | None = None


# --- Histologie / biologie moléculaire --------------------------------------


class HistologieCreate(BaseModel):
    preuve_histologique: bool = False
    statut_brca_germinal: str = "non_teste"
    statut_kras: str = "non_teste"
    statut_msi_dmmr: str = "non_teste"
    fusion_ntrk: str = "non_teste"
    fusion_nrg1: str = "non_teste"


class HistologieUpdate(BaseModel):
    preuve_histologique: bool | None = None
    statut_brca_germinal: str | None = None
    statut_kras: str | None = None
    statut_msi_dmmr: str | None = None
    fusion_ntrk: str | None = None
    fusion_nrg1: str | None = None


class HistologieRead(HistologieCreate):
    model_config = ConfigDict(from_attributes=True)

    id_histo: int
    id_evaluation: int


# --- Analyse moléculaire -----------------------------------------------------


class AnalyseCreate(BaseModel):
    type_test: str | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: str | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


class AnalyseUpdate(BaseModel):
    type_test: str | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: str | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


class AnalyseRead(AnalyseCreate):
    model_config = ConfigDict(from_attributes=True)

    id_analyse: int
    id_evaluation: int


# --- Comorbidité (liaison) ----------------------------------------------------


class ComorbiditeEvaluationCreate(BaseModel):
    id_comorbidite: int
    severite: str = "mineure"
    note: str | None = None


class ComorbiditeEvaluationUpdate(BaseModel):
    severite: str | None = None
    note: str | None = None


class ComorbiditeEvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_evaluation: int
    id_comorbidite: int
    severite: str | None = None
    note: str | None = None
