from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class DetailPatient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_patient: int
    nom: str
    prenom: str
    date_naissance: date | None = None
    sexe: str | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None


class DetailAntecedent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_antecedent: int
    degre_parente: str | None = None
    nombre_apparentes: int | None = None
    type_cancer: str | None = None


class DetailMutation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_mutation: int
    id_gene: int
    statut: str | None = None
    date_test: date | None = None


class DetailBiologie(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_biologie: int
    ca19_9: Decimal | None = None
    ca19_9_multiple_lsn: Decimal | None = None
    cholestase: bool | None = None
    bilirubine: Decimal | None = None
    bilirubine_ratio_lsn: Decimal | None = None
    statut_lewis: str | None = None
    statut_dpd: str | None = None
    albuminemie: Decimal | None = None
    date_analyse: date | None = None


class DetailMetastase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_metastase: int
    site: str
    detail: str | None = None


class DetailImagerie(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_imagerie: int
    type_imagerie: str
    date_imagerie: date
    localisation_tumorale: str | None = None
    taille_tumorale_cm: Decimal | None = None
    contact_ams: str | None = None
    contact_tronc_coeliaque: str | None = None
    contact_art_hepatique: str | None = None
    contact_vms_vp: str | None = None
    extension_ganglionnaire_regionale: bool | None = None
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None
    metastases: list[DetailMetastase] = []


class DetailHistologie(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_histo: int
    preuve_histologique: bool | None = None
    statut_brca_germinal: str | None = None
    statut_kras: str | None = None
    statut_msi_dmmr: str | None = None
    fusion_ntrk: str | None = None
    fusion_nrg1: str | None = None


class DetailAnalyse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_analyse: int
    type_test: str | None = None
    gene: str | None = None
    alteration: str | None = None
    classe_escat: str | None = None
    date_test: date | None = None
    reference_rapport: str | None = None


class DetailComorbidite(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_comorbidite: int
    severite: str | None = None
    note: str | None = None


class DetailDecision(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_decision: int
    date_decision: datetime
    decide_par: int | None = None
    source_code: str | None = None
    source_version: str | None = None
    resume: str | None = None
    decision_medecin: str | None = None
    necessite_rcp: bool | None = None


class DetailEvaluation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_evaluation: int
    date_evaluation: date
    contexte: str | None = None
    ecog: int | None = None
    etat_nutritionnel: str | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    diabete: str | None = None
    date_creation: datetime
    biologie: DetailBiologie | None = None
    histologie: DetailHistologie | None = None
    imageries: list[DetailImagerie] = []
    analyses: list[DetailAnalyse] = []
    comorbidites: list[DetailComorbidite] = []
    decisions: list[DetailDecision] = []


class DetailTraitement(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_traitement: int
    id_protocole: int | None = None
    numero_ligne: int | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    reponse: str | None = None
    toxicite_residuelle: bool | None = None
    type_toxicite: str | None = None
    termine_comme_prevu: bool | None = None
    notes: str | None = None


class DossierDetailRead(BaseModel):
    id_dossier: int
    statut: str
    date_creation: datetime
    date_modification: datetime
    patient: DetailPatient
    antecedents: list[DetailAntecedent] = []
    mutations: list[DetailMutation] = []
    evaluations: list[DetailEvaluation] = []
    traitements: list[DetailTraitement] = []
