from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


# --- Évaluation clinique ----------------------------------------------------


class EvaluationCreate(BaseModel):
    date_evaluation: date
    contexte: Literal["diagnostic", "pre_neoadjuvant", "restaging", "pre_chirurgie", "adjuvant", "surveillance", "recidive"] = "diagnostic"
    ecog: int | None = None
    etat_nutritionnel: Literal["normal", "denutrition_moderee", "denutrition_severe", "inconnu"] = "inconnu"
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: Literal["absent", "recent_moins_2ans", "ancien", "inconnu"] = "inconnu"


class EvaluationUpdate(BaseModel):
    date_evaluation: date | None = None
    contexte: Literal["diagnostic", "pre_neoadjuvant", "restaging", "pre_chirurgie", "adjuvant", "surveillance", "recidive"] | None = None
    ecog: int | None = None
    etat_nutritionnel: Literal["normal", "denutrition_moderee", "denutrition_severe", "inconnu"] | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: Literal["absent", "recent_moins_2ans", "ancien", "inconnu"] | None = None


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
    statut_lewis: Literal["exprime", "a_b_negatif", "inconnu"] = "inconnu"
    statut_dpd: Literal["normal", "deficit_partiel", "deficit_complet", "non_teste"] = "non_teste"
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieUpdate(BaseModel):
    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: Literal["exprime", "a_b_negatif", "inconnu"] | None = None
    statut_dpd: Literal["normal", "deficit_partiel", "deficit_complet", "non_teste"] | None = None
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class BiologieRead(BiologieCreate):
    model_config = ConfigDict(from_attributes=True)

    id_biologie: int
    id_evaluation: int


# --- Imagerie ----------------------------------------------------------------


class ImagerieCreate(BaseModel):
    type_imagerie: Literal["TDM", "IRM"]
    date_imagerie: date
    localisation_tumorale: Literal["tete_crochet", "corps_queue", "inconnu"] = "inconnu"
    taille_tumorale_cm: Decimal | None = None
    contact_ams: Literal["absent", "lt180", "ge180"] | None = None
    contact_tronc_coeliaque: Literal["absent", "lt180", "ge180"] | None = None
    contact_art_hepatique: Literal["absent", "court_sans_envahissement", "envahissant"] | None = None
    contact_vms_vp: Literal["absent", "lt180_sans_irregularite", "ge180_ou_irregularite", "occlusion_reconstructible", "occlusion_non_reconstructible"] | None = None
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
    statut_brca_germinal: Literal["mute", "non_mute", "non_teste"] = "non_teste"
    statut_kras: Literal["sauvage", "g12c", "g12d", "g12v", "autre_mute", "non_teste"] = "non_teste"
    statut_msi_dmmr: Literal["mss", "msi_h", "dmmr", "non_teste"] = "non_teste"
    fusion_ntrk: Literal["positif", "negatif", "non_teste"] = "non_teste"
    fusion_nrg1: Literal["positif", "negatif", "non_teste"] = "non_teste"

    @field_validator("statut_brca_germinal", mode="before")
    @classmethod
    def normalize_brca(cls, value: object) -> object:
        return {"muté": "mute", "non muté": "non_mute", "non testé": "non_teste"}.get(value, value)

    @field_validator("statut_kras", mode="before")
    @classmethod
    def normalize_kras(cls, value: object) -> object:
        return {"G12C": "g12c", "G12D": "g12d", "G12V": "g12v", "autre": "autre_mute", "non testé": "non_teste"}.get(value, value)

    @field_validator("statut_msi_dmmr", mode="before")
    @classmethod
    def normalize_msi(cls, value: object) -> object:
        return {"positif": "msi_h", "négatif": "mss", "non testé": "non_teste"}.get(value, value)

    @field_validator("fusion_ntrk", "fusion_nrg1", mode="before")
    @classmethod
    def normalize_fusion(cls, value: object) -> object:
        return {"oui": "positif", "non": "negatif", "non testé": "non_teste"}.get(value, value)


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
