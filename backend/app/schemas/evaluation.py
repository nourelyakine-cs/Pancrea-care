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
    ecog: int | None = Field(default=None, ge=0, le=4)
    etat_nutritionnel: EtatNutritionnel = "inconnu"
    douleur_presente: bool | None = None
    intensite_douleur: int | None = Field(default=None, ge=0, le=10)
    ictere: bool | None = None
    diabete: Diabete = "inconnu"


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


# --- Métastase ---------------------------------------------------------------


class MetastaseCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    site: SiteMetastase
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


# --- Analyse moléculaire -----------------------------------------------------


class AnalyseCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type_test: TypeTest | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: ClasseEscat | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


# --- Comorbidité (liaison) ----------------------------------------------------


class ComorbiditeEvaluationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id_comorbidite: int
    severite: Severite = "mineure"
    note: str | None = None


# --- Parcours thérapeutique --------------------------------------------------
class ParcoursTherapeutiqueCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    angiocholite: bool | None = None
    comorbidites_lourdes: bool | None = None
    tumeur_controlee: bool | None = None
    nouvelles_metastases: bool | None = None
    chirurgie_d_emblee: bool | None = None
    traitement_medical_prevu: bool | None = None
    pas_de_progression_apres_16_semaines_platine: bool | None = None
    date_reevaluation: date | None = None
    commentaire: str | None = None


# --- Résumé des évaluations d'un patient (historique / "Toutes évaluations") ---


class EvaluationResumeRead(BaseModel):
    """Évaluation d'un patient enrichie du médecin évaluateur et du dernier
    calcul de DonneesDerivees (stade TNM, résécabilité, critères ABC)."""

    id_evaluation: int
    id_dossier: int
    date_evaluation: date
    contexte: str | None = None
    ecog: int | None = None
    etat_nutritionnel: str | None = None
    douleur_presente: bool | None = None
    ictere: bool | None = None
    date_creation: datetime

    medecin_nom: str | None = None
    medecin_prenom: str | None = None

    stade_global: str | None = None
    resecabilite: str | None = None
    categorie_t: str | None = None
    categorie_n: str | None = None
    categorie_m: str | None = None
    sous_categorie_abc: str | None = None
    date_calcul: datetime | None = None
