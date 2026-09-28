from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class PatientDetailRead(BaseModel):
    """Fiche consolidée d'un patient pour l'écran « Voir Détails ».

    Rassemble en une seule requête tout ce qui est affiché par la modale :
    identité, dernière évaluation (clinique, biologie, imagerie, histologie,
    parcours thérapeutique) et dernier bilan CDSS (stade TNM, résécabilité,
    critères ABC). Les champs non renseignés restent `None` : la modale les
    affiche alors comme « non renseigné » plutôt que « Non ».
    """

    # --- A.1 Démographie -----------------------------------------------------
    id_patient: int
    nom: str
    prenom: str
    date_naissance: date | None = None
    age: int | None = None
    sexe: str | None = None
    telephone: str | None = None
    email: EmailStr | None = None
    adresse: str | None = None

    # --- Dossier & évaluation de référence -----------------------------------
    id_dossier: int | None = None
    statut_dossier: str | None = None
    id_evaluation: int | None = None
    date_derniere_evaluation: date | None = None
    contexte: str | None = None

    # --- A.2 État clinique ---------------------------------------------------
    ecog: int | None = None
    etat_nutritionnel: str | None = None
    douleur_presente: bool | None = None
    intensite_douleur: int | None = None
    ictere: bool | None = None
    angiocholite: bool | None = None
    cholestase: bool | None = None
    diabete: str | None = None
    comorbidites_lourdes: bool = False
    comorbidites: list[str] = []

    # --- A.3 Biologie --------------------------------------------------------
    ca19_9: float | None = None
    ca19_9_multiple_lsn: float | None = None
    bilirubine: float | None = None
    bilirubine_ratio_lsn: float | None = None
    statut_dpd: str | None = None
    albuminemie: float | None = None

    # --- A.4 Imagerie (examen le plus récent) --------------------------------
    id_imagerie: int | None = None
    type_imagerie: str | None = None
    date_imagerie: date | None = None
    localisation_tumorale: str | None = None
    taille_tumorale_cm: float | None = None
    contact_ams: str | None = None
    contact_tronc_coeliaque: str | None = None
    contact_art_hepatique: str | None = None
    contact_vms_vp: str | None = None
    extension_ganglionnaire_regionale: bool | None = None
    extension_ganglionnaire_distance: bool | None = None
    metastases_presentes: bool | None = None
    sites_metastases: list[str] = []

    # --- TNM & dernier bilan CDSS -------------------------------------------
    categorie_t: str | None = None
    categorie_n: str | None = None
    categorie_m: str | None = None
    stade_global: str | None = None
    resecabilite: str | None = None
    critere_abc_a: str | None = None
    critere_abc_b: bool | None = None
    critere_abc_c: bool | None = None
    sous_categorie_abc: str | None = None
    date_calcul: datetime | None = None

    # --- A.6 Histologie & biologie moléculaire -------------------------------
    preuve_histologique: bool | None = None
    statut_brca_germinal: str | None = None
    statut_kras: str | None = None
    statut_msi_dmmr: str | None = None
    fusion_ntrk: str | None = None
    fusion_nrg1: str | None = None

    # --- A.7 Parcours thérapeutique ------------------------------------------
    ligne_traitement_actuelle: int | None = None
    reponse_traitement_en_cours: str | None = None
    traitements_recus: list[str] = []
    traitements_recus_texte: str | None = None
    ligne_precedente: str | None = None
    duree_chimiotherapie_mois: float | None = None
    tumeur_controlee: bool | None = None
    nouvelles_metastases: bool | None = None
    chirurgie_d_emblee: bool | None = None
    traitement_medical_prevu: bool | None = None
    pas_de_progression_apres_16_semaines_platine: bool | None = None
    toxicite_residuelle: bool | None = None
    details_toxicite: str | None = None
