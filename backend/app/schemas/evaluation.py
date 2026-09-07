from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    ClasseEscat,
    ContexteEvaluation,
    ContactArtHepatique,
    ContactVaisseau,
    ContactVmsVp,
    Diabete,
    EtatNutritionnel,
    Fusion,
    LocalisationTumorale,
    Severite,
    SiteMetastase,
    StatutBrca,
    StatutDpd,
    StatutKras,
    StatutLewis,
    StatutMsi,
    TypeImagerie,
    TypeTest,
)


# --- Évaluation clinique ----------------------------------------------------


class EvaluationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    date_evaluation: date
    contexte: ContexteEvaluation = "diagnostic"
    ecog: int | None = Field(default=None, ge=0, le=5)
    etat_nutritionnel: EtatNutritionnel = "inconnu"
    douleur_presente: bool | None = None
    intensite_douleur: int | None = Field(default=None, ge=0, le=10)
    ictere: bool | None = None
    diabete: Diabete = "inconnu"


class EvaluationUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    date_evaluation: date | None = None
    contexte: ContexteEvaluation | None = None
    ecog: int | None = Field(default=None, ge=0, le=5)
    etat_nutritionnel: EtatNutritionnel | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = Field(default=None, ge=0, le=10)
    ictere: bool | None = None
    diabete: Diabete | None = None


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_evaluation: int
    id_dossier: int
    id_medecin_evaluateur: int | None = None
    date_evaluation: date
    contexte: ContexteEvaluation | None = None
    ecog: int | None = None
    etat_nutritionnel: EtatNutritionnel | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: Diabete | None = None
    date_creation: datetime


# --- Biologie ----------------------------------------------------------------


class BiologieCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: StatutLewis = "inconnu"
    statut_dpd: StatutDpd = "non_teste"
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: StatutLewis | None = None
    statut_dpd: StatutDpd | None = None
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieRead(BiologieCreate):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_biologie: int
    id_evaluation: int


# --- Imagerie ----------------------------------------------------------------


class ImagerieCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type_imagerie: TypeImagerie
    date_imagerie: date
    localisation_tumorale: LocalisationTumorale = "inconnu"
    taille_tumorale_cm: Decimal | None = None
    contact_ams: ContactVaisseau | None = None
    contact_tronc_coeliaque: ContactVaisseau | None = None
    contact_art_hepatique: ContactArtHepatique | None = None
    contact_vms_vp: ContactVmsVp | None = None
    extension_ganglionnaire_regionale: bool = False
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None


class ImagerieUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type_imagerie: TypeImagerie | None = None
    date_imagerie: date | None = None
    localisation_tumorale: LocalisationTumorale | None = None
    taille_tumorale_cm: Decimal | None = None
    contact_ams: ContactVaisseau | None = None
    contact_tronc_coeliaque: ContactVaisseau | None = None
    contact_art_hepatique: ContactArtHepatique | None = None
    contact_vms_vp: ContactVmsVp | None = None
    extension_ganglionnaire_regionale: bool | None = None
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None


class ImagerieRead(ImagerieCreate):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_imagerie: int
    id_evaluation: int


# --- Métastase ---------------------------------------------------------------


class MetastaseCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    site: SiteMetastase
    detail: str | None = None


class MetastaseUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    site: SiteMetastase | None = None
    detail: str | None = None


class MetastaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_metastase: int
    id_imagerie: int
    site: SiteMetastase | None = None
    detail: str | None = None


# --- Histologie / biologie moléculaire --------------------------------------


class HistologieCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    preuve_histologique: bool = False
    statut_brca_germinal: StatutBrca = "non_teste"
    statut_kras: StatutKras = "non_teste"
    statut_msi_dmmr: StatutMsi = "non_teste"
    fusion_ntrk: Fusion = "non_teste"
    fusion_nrg1: Fusion = "non_teste"


class HistologieUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    preuve_histologique: bool | None = None
    statut_brca_germinal: StatutBrca | None = None
    statut_kras: StatutKras | None = None
    statut_msi_dmmr: StatutMsi | None = None
    fusion_ntrk: Fusion | None = None
    fusion_nrg1: Fusion | None = None


class HistologieRead(HistologieCreate):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_histo: int
    id_evaluation: int


# --- Analyse moléculaire -----------------------------------------------------


class AnalyseCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type_test: TypeTest | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: ClasseEscat | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


class AnalyseUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type_test: TypeTest | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: ClasseEscat | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


class AnalyseRead(AnalyseCreate):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_analyse: int
    id_evaluation: int


# --- Comorbidité (liaison) ----------------------------------------------------


class ComorbiditeEvaluationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_comorbidite: int
    severite: Severite = "mineure"
    note: str | None = None


class ComorbiditeEvaluationUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    severite: Severite | None = None
    note: str | None = None


class ComorbiditeEvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id_evaluation: int
    id_comorbidite: int
    severite: Severite | None = None
    note: str | None = None