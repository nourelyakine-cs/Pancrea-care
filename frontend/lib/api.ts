const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, body?: unknown, method: "GET" | "POST" | "PUT" | "DELETE" = body ? "POST" : "GET"): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      method,
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (cause) {
    const reason = cause instanceof Error ? ` (${cause.message})` : "";
    throw new Error(`Impossible de joindre le serveur [${method} ${path}].${reason}`);
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail ?? "Une erreur est survenue.");
  return data as T;
}

export const login = (email: string, password: string) =>
  request<{ access_token: string }>("/auth/login", { email, password });

export const signup = (payload: {
  nom: string;
  prenom: string;
  email: string;
  password: string;
  telephone?: string;
  hopital?: string;
}) => request<{ user: string; medecin_id: number; need_email_confirmation: boolean }>("/auth/signup", payload);

export const forgotPassword = (email: string) =>
  request<{ message: string }>("/auth/forgot-password", { email });

export const resetPassword = (access_token: string, refresh_token: string, new_password: string) =>
  request<{ message: string }>("/auth/reset-password", { access_token, refresh_token, new_password });

// Règles de mot de passe appliquées par l'API : le formulaire les consomme
// pour afficher au médecin ce qu'il reste à respecter avant l'envoi.
export interface PasswordPolicy {
  min_length: number;
  require_lowercase: boolean;
  require_uppercase: boolean;
  require_digit: boolean;
}

// Règles par défaut, identiques à celles du backend. Servent de repli si
// l'endpoint est injoignable : l'utilisateur voit les exigences plutôt qu'un
// formulaire muet.
export const DEFAULT_PASSWORD_POLICY: PasswordPolicy = {
  min_length: 8,
  require_lowercase: true,
  require_uppercase: true,
  require_digit: true,
};

export const getPasswordPolicy = () =>
  request<PasswordPolicy>("/auth/password-policy", undefined, "GET").catch(() => DEFAULT_PASSWORD_POLICY);

// --- Types backend (schemas Pydantic) ---------------------------------------

export interface FullPatientRead {
  id_patient: number;
  id_dossier: number;
  id_evaluation: number;
  id_decision: number;
  date_creation: string;
}

export interface PatientListItem {
  id_patient: number;
  nom: string;
  prenom: string;
  date_naissance: string | null;
  sexe: "M" | "F" | "inconnu" | null;
  telephone: string | null;
  email: string | null;
  adresse: string | null;
  date_creation: string;
  date_modification: string;
  id_dossier: number | null;
  id_evaluation: number | null;
  date_derniere_evaluation: string | null;
  stade_global: string | null;
  resecabilite: string | null;
  categorie_t: string | null;
  categorie_n: string | null;
  categorie_m: string | null;
}

export const getPatients = (nom?: string) =>
  request<PatientListItem[]>(
    `/patients${nom ? `?nom=${encodeURIComponent(nom)}` : ""}`,
    undefined,
    "GET",
  );

export interface PatientRead {
  id_patient: number;
  nom: string;
  prenom: string;
  date_naissance: string | null;
  sexe: "M" | "F" | "inconnu" | null;
  telephone: string | null;
  email: string | null;
  adresse: string | null;
  date_creation: string;
  date_modification: string;
}

export const getPatient = (idPatient: number | string) =>
  request<PatientRead>(`/patients/${idPatient}`, undefined, "GET");

export const updatePatient = (
  idPatient: number | string,
  payload: {
    nom?: string;
    prenom?: string;
    date_naissance?: string | null;
    sexe?: string | null;
    telephone?: string | null;
    adresse?: string | null;
  },
) => request<PatientRead>(`/patients/${idPatient}`, payload, "PUT");

// Fiche consolidée d'un patient pour l'écran « Voir Détails ».
export interface PatientDetail {
  id_patient: number;
  nom: string;
  prenom: string;
  date_naissance: string | null;
  age: number | null;
  sexe: string | null;
  telephone: string | null;
  email: string | null;
  adresse: string | null;

  id_dossier: number | null;
  statut_dossier: string | null;
  id_evaluation: number | null;
  date_derniere_evaluation: string | null;
  contexte: string | null;

  ecog: number | null;
  etat_nutritionnel: string | null;
  douleur_presente: boolean | null;
  intensite_douleur: number | null;
  ictere: boolean | null;
  angiocholite: boolean | null;
  cholestase: boolean | null;
  diabete: string | null;
  comorbidites_lourdes: boolean;
  comorbidites: string[];

  ca19_9: number | null;
  ca19_9_multiple_lsn: number | null;
  bilirubine: number | null;
  bilirubine_ratio_lsn: number | null;
  statut_dpd: string | null;
  albuminemie: number | null;

  id_imagerie: number | null;
  type_imagerie: string | null;
  date_imagerie: string | null;
  localisation_tumorale: string | null;
  taille_tumorale_cm: number | null;
  contact_ams: string | null;
  contact_tronc_coeliaque: string | null;
  contact_art_hepatique: string | null;
  contact_vms_vp: string | null;
  extension_ganglionnaire_regionale: boolean | null;
  extension_ganglionnaire_distance: boolean | null;
  metastases_presentes: boolean | null;
  sites_metastases: string[];

  categorie_t: string | null;
  categorie_n: string | null;
  categorie_m: string | null;
  stade_global: string | null;
  resecabilite: string | null;
  critere_abc_a: string | null;
  critere_abc_b: boolean | null;
  critere_abc_c: boolean | null;
  sous_categorie_abc: string | null;
  date_calcul: string | null;

  preuve_histologique: boolean | null;
  statut_brca_germinal: string | null;
  statut_kras: string | null;
  statut_msi_dmmr: string | null;
  fusion_ntrk: string | null;
  fusion_nrg1: string | null;

  ligne_traitement_actuelle: number | null;
  reponse_traitement_en_cours: string | null;
  traitements_recus: string[];
  traitements_recus_texte: string | null;
  ligne_precedente: string | null;
  duree_chimiotherapie_mois: number | null;
  tumeur_controlee: boolean | null;
  nouvelles_metastases: boolean | null;
  chirurgie_d_emblee: boolean | null;
  traitement_medical_prevu: boolean | null;
  pas_de_progression_apres_16_semaines_platine: boolean | null;
  toxicite_residuelle: boolean | null;
  details_toxicite: string | null;
}

export const getPatientDetail = (idPatient: number | string) =>
  request<PatientDetail>(`/patients/${idPatient}/detail`, undefined, "GET");

export interface DetailBiologie {
  ca19_9: number | null;
  cholestase: boolean | null;
  bilirubine: number | null;
  bilirubine_ratio_lsn: number | null;
  statut_dpd: string | null;
  albuminemie: number | null;
}

export interface DetailHistologie {
  preuve_histologique: boolean | null;
  statut_brca_germinal: string | null;
  statut_kras: string | null;
  statut_msi_dmmr: string | null;
  fusion_ntrk: string | null;
  fusion_nrg1: string | null;
}

export interface DetailImagerie {
  type_imagerie: string;
  date_imagerie: string;
  localisation_tumorale: string | null;
  taille_tumorale_cm: number | null;
  contact_ams: string | null;
  contact_tronc_coeliaque: string | null;
  contact_art_hepatique: string | null;
  contact_vms_vp: string | null;
  extension_ganglionnaire_regionale: boolean | null;
  extension_ganglionnaire_distance: boolean | null;
  metastases_presentes: boolean | null;
}

export interface DetailEvaluation {
  id_evaluation: number;
  date_evaluation: string;
  contexte: string | null;
  ecog: number | null;
  etat_nutritionnel: string | null;
  douleur_presente: boolean | null;
  intensite_douleur: number | null;
  ictere: boolean | null;
  diabete: string | null;
  date_creation: string;
  biologie: DetailBiologie | null;
  histologie: DetailHistologie | null;
  imageries: DetailImagerie[];
}

export interface DossierDetail {
  id_dossier: number;
  statut: string;
  date_creation: string;
  date_modification: string;
  patient: PatientRead;
  evaluations: DetailEvaluation[];
}

export const getDossierDetail = (idDossier: number | string) =>
  request<DossierDetail>(`/dossiers/full/${idDossier}`, undefined, "GET");

export interface EvaluationResume {
  id_evaluation: number;
  id_dossier: number;
  date_evaluation: string;
  contexte: string | null;
  ecog: number | null;
  etat_nutritionnel: string | null;
  douleur_presente: boolean | null;
  ictere: boolean | null;
  date_creation: string;
  medecin_nom: string | null;
  medecin_prenom: string | null;
  stade_global: string | null;
  resecabilite: string | null;
  categorie_t: string | null;
  categorie_n: string | null;
  categorie_m: string | null;
  sous_categorie_abc: string | null;
  date_calcul: string | null;
}

export interface ClinicalResult {
  id_derive: number;
  id_evaluation: number;
  version_moteur: string;
  source_code: string;
  source_version: string;
  date_calcul: string;
  resecabilite: string | null;
  categorie_t: string | null;
  categorie_n: string | null;
  categorie_m: string | null;
  stade_global: string | null;
  critere_abc_a: string | null;
  critere_abc_b: boolean | null;
  critere_abc_c: boolean | null;
  sous_categorie_abc: string | null;
  justification_calcul: string | null;
}

export interface RecommendationItem {
  code: string;
  titre?: string | null;
  conclusion: string;
  reference: string;
  grade: string;
  criteres_evalues: Record<string, any>;
}

export interface DecisionPathStep {
  code: string;
  statut: string;
  motif?: string | null;
  champs_manquants?: string[] | null;
  reference?: string | null;
  grade?: string | null;
  criteres_evalues?: Record<string, unknown> | null;
  nombre_conclusions?: number | null;
}

export interface RecommendationsResponse {
  facts: Record<string, any>;
  recommendations: RecommendationItem[];
  regles_declenchees: string[];
  decision_path: DecisionPathStep[];
  necessite_rcp?: boolean;
  source_code?: string;
  source_version?: string;
  date_decision?: string | null;
  id_evaluation?: number;
}

// --- Mapping formulaire (camelCase FR) -> enums backend (snake_case) ---------

const ENUM_MAP: Record<string, Record<string, string>> = {
  etatNutritionnel: {
    "dénutrition modérée": "denutrition_moderee",
    "dénutrition sévère": "denutrition_severe",
  },
  diabete: { "récent (<2 ans)": "recent_moins_2ans" },
  statutDpd: {
    "déficit partiel": "deficit_partiel",
    "déficit complet": "deficit_complet",
  },
  localisationTumorale: {
    "tête/crochet": "tete_crochet",
    "corps-queue": "corps_queue",
  },
  contactAms: { "pas de contact": "absent", "<180°": "lt180", "≥180°": "ge180" },
  contactTroncCoeliaque: { "pas de contact": "absent", "<180°": "lt180", "≥180°": "ge180" },
  contactAhc: {
    "pas de contact": "absent",
    "court reconstructible": "court_sans_envahissement",
    "non reconstructible": "envahissant",
  },
  contactVmsVp: {
    "<180° sans irrégularité": "lt180_sans_irregularite",
    "≥180° ou irrégularité ou occlusion reconstructible": "ge180_ou_irregularite",
    "occlusion non reconstructible": "occlusion_non_reconstructible",
  },
  statutBrca: { "non testé": "non_teste", "muté": "mute", "non muté": "non_mute" },
  statutKras: {
    "non testé": "non_teste",
    "G12C": "g12c",
    "G12D": "g12d",
    "G12V": "g12v",
    "autre": "autre_mute",
  },
  statutMsiDmmr: { "non testé": "non_teste", "positif": "msi_h", "négatif": "mss" },
  fusionNtrk: { "non testé": "non_teste", "oui": "positif", "non": "negatif" },
  fusionNrg1: { "non testé": "non_teste", "oui": "positif", "non": "negatif" },
};

const toEnum = (value: string | null | undefined, key: string): string | null => {
  if (value == null || value === "") return null;
  if (key === "statutDpd" && value === "normal") return "normal";
  return ENUM_MAP[key]?.[value] ?? value;
};

const toNumber = (value: unknown): number | null => {
  if (value == null || value === "") return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
};

function buildEvaluationPayload(data: Record<string, any>) {
  const today = new Date().toISOString().slice(0, 10);
  const bilirubine = toNumber(data.bilirubine);
  const lsnBilirubine = toNumber(data.lsnBilirubine);
  const bilirubine_ratio_lsn = bilirubine != null && lsnBilirubine && lsnBilirubine > 0 ? bilirubine / lsnBilirubine : null;

  const metastases_presentes = Boolean(data.metastases);
  const duree = toNumber(data.dureeChimiotherapieMois);
  const dateDebutCourante = duree != null
    ? new Date(Date.now() - duree * 30.4375 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10)
    : null;
  const reponseTraitementPrecedent = data.reponseTraitementPrecedent || data.reponseTraitementEnCours || null;
  const currentLine = Number(data.ligneTraitementActuelle || 1);
  const received = Array.isArray(data.traitementsRecus)
    ? data.traitementsRecus.filter(Boolean)
    : [];

  if (currentLine >= 2 && received.length === 0) {
    throw new Error(
      "Le traitement précédent est obligatoire à partir de la deuxième ligne."
    );
  }

  if (currentLine >= 2 && !reponseTraitementPrecedent) {
    throw new Error(
      "La réponse au traitement précédent est obligatoire à partir de la deuxième ligne."
    );
  }

  if (duree == null) {
    throw new Error("La durée de la chimiothérapie doit être renseignée.");
  }

  const previousTreatments = received.map((name: string, index: number) => ({
    numero_ligne: Math.max(1, currentLine - received.length + index),
    date_debut: null,
    date_fin: null,
    reponse: index === received.length - 1
      ? reponseTraitementPrecedent
      : null,
    toxicite_residuelle: false,
    type_toxicite: null,
    termine_comme_prevu: null,
    notes: name,
  }));

  const traitements = [
    ...previousTreatments,
    {
      numero_ligne: currentLine,
      date_debut: dateDebutCourante,
      date_fin: null,
      reponse: null,
      toxicite_residuelle: Boolean(data.toxiciteResiduelle),
      type_toxicite: data.detailsToxicite || null,
      termine_comme_prevu: null,
      notes: null,
    },
  ];

  return {
    date_evaluation: today,
    contexte: "diagnostic",
    ecog: data.ecog ?? null,
    etat_nutritionnel: toEnum(data.etatNutritionnel, "etatNutritionnel") ?? "inconnu",
    douleur_presente: data.douleur === "présente" ? true : data.douleur === "absente" ? false : null,
    intensite_douleur: data.intensiteDouleur ? toNumber(data.intensiteDouleur) ?? null : null,
    ictere: Boolean(data.ictere),
    diabete: toEnum(data.diabete, "diabete") ?? "inconnu",
    biologie: {
      ca19_9: toNumber(data.ca199),
      cholestase: Boolean(data.cholestase),
      bilirubine,
      bilirubine_ratio_lsn,
      statut_dpd: toEnum(data.statutDpd, "statutDpd") ?? "non_teste",
      albuminemie: toNumber(data.albuminemie),
    },
    imageries: [
      {
        type_imagerie: "TDM",
        date_imagerie: today,
        localisation_tumorale: toEnum(data.localisationTumorale, "localisationTumorale") ?? "inconnu",
        taille_tumorale_cm: toNumber(data.tailleTumorale),
        contact_ams: toEnum(data.contactAms, "contactAms"),
        contact_tronc_coeliaque: toEnum(data.contactTroncCoeliaque, "contactTroncCoeliaque"),
        contact_art_hepatique: toEnum(data.contactAhc, "contactAhc"),
        contact_vms_vp: toEnum(data.contactVmsVp, "contactVmsVp"),
        extension_ganglionnaire_regionale: Boolean(data.adenopathieRegionale),
        extension_ganglionnaire_distance: Boolean(data.adenopathieDistance),
        metastases_presentes,
        metastases: metastases_presentes
          ? (data.sitesMetastases?.length
            ? data.sitesMetastases.map((site: string) => ({ site, detail: null }))
            : [{ site: "autre", detail: null }])
          : [],
      },
    ],
    histologie: {
      preuve_histologique: Boolean(data.preuveHistologique),
      statut_brca_germinal: toEnum(data.statutBrca, "statutBrca") ?? "non_teste",
      statut_kras: toEnum(data.statutKras, "statutKras") ?? "non_teste",
      statut_msi_dmmr: toEnum(data.statutMsiDmmr, "statutMsiDmmr") ?? "non_teste",
      fusion_ntrk: toEnum(data.fusionNtrk, "fusionNtrk") ?? "non_teste",
      fusion_nrg1: toEnum(data.fusionNrg1, "fusionNrg1") ?? "non_teste",
    },
    analyses: [],
    comorbidites: [],
    parcours: {
      angiocholite: data.angiocholite ?? null,
      comorbidites_lourdes: data.comorbiditesLourdes ?? null,
      tumeur_controlee: data.tumeurControle ?? null,
      nouvelles_metastases: data.nouvellesMetastases ?? null,
      chirurgie_d_emblee: data.chirurgieDembleePrevue ?? null,
      traitement_medical_prevu: data.traitementMedicalPrevu ?? null,
      pas_de_progression_apres_16_semaines_platine: data.pasDeProgressionApres16SemainesPlatine ?? null,
      date_reevaluation: today,
      commentaire: null,
    },
    traitements,
  };
}

function buildFullPatientPayload(data: Record<string, any>) {
  return {
    nom: data.nom,
    prenom: data.prenom,
    date_naissance: data.dateNaissance || null,
    sexe: data.sexe || null,
    telephone: data.telephone || null,
    adresse: data.adresse || null,
    antecedents: [],
    mutations: [],
    evaluation: buildEvaluationPayload(data),
  };
}

// --- Création patient + calcul CDSS -----------------------------------------

export const createPatientAndCalculate = async (formData: Record<string, any>) => {
  const created = await request<FullPatientRead>("/patients/full", buildFullPatientPayload(formData));
  const calculated = await request<ClinicalResult>(
    `/clinical-rules/evaluations/${created.id_evaluation}/calculate`,
    {
      categorie_t: formData.categorieT,
      categorie_n: formData.categorieN,
      categorie_m: formData.categorieM,
      version_moteur: "tncd-2024-v1",
    }
  );
  return { created, calculated };
};

export const createEvaluationAndCalculate = async (
  idPatient: number | string,
  formData: Record<string, any>,
) => {
  const created = await request<FullPatientRead>(
    `/patients/${idPatient}/evaluations`,
    buildEvaluationPayload(formData),
  );
  const calculated = await request<ClinicalResult>(
    `/clinical-rules/evaluations/${created.id_evaluation}/calculate`,
    {
      categorie_t: formData.categorieT,
      categorie_n: formData.categorieN,
      categorie_m: formData.categorieM,
      version_moteur: "tncd-2024-v1",
    }
  );
  return { created, calculated };
};

export const getRecommendations = (idEvaluation: number) =>
  request<RecommendationsResponse>(
    `/clinical-rules/evaluations/${idEvaluation}/recommendations`,
    undefined,
    "GET"
  );

export const getPatientEvaluations = (idPatient: number | string) =>
  request<EvaluationResume[]>(`/patients/${idPatient}/evaluations`, undefined, "GET");