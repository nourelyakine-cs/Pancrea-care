export type ClinicalResult = {
  id_derive: number;
  id_evaluation: number;
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
};

export type FullCreationResult = {
  id_patient: number;
  id_dossier: number;
  id_evaluation: number;
  id_decision: number;
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

async function request<T>(path: string, init: RequestInit): Promise<T> {
  const token = typeof window !== "undefined" ? window.localStorage.getItem("pancrea_access_token") : null;
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(init.headers || {}) },
    });
  } catch {
    throw new Error(`Backend inaccessible (${API_URL}). Vérifiez que FastAPI est lancé et que NEXT_PUBLIC_API_URL est correct.`);
  }
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = body?.detail || `Erreur HTTP ${response.status}`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return body as T;
}

const today = () => new Date().toISOString().slice(0, 10);
const numberOrNull = (value: unknown) => value === "" || value == null ? null : Number(value);
const nutritionValue = (value: string) => ({
  "dénutrition sévère": "denutrition_severe",
  "dénutrition modérée": "denutrition_moderee",
}[value] || value);
const contactArteriel = (value: string) => value === "pas de contact" ? "absent" : value === "<180°" ? "lt180" : "ge180";
const contactAhc = (value: string) => value === "pas de contact" ? "absent" : value === "court reconstructible" ? "court_sans_envahissement" : "envahissant";
const contactVeineux = (value: string) => value === "<180° sans irrégularité" ? "lt180_sans_irregularite" : value === "occlusion non reconstructible" ? "occlusion_non_reconstructible" : "ge180_ou_irregularite";
const dpdValue = (value: string) => ({
  "déficit partiel": "deficit_partiel",
  "déficit complet": "deficit_complet",
  normal: "normal",
}[value] || "non_teste");
const diabetesValue = (value: string) => ({
  "récent (<2 ans)": "recent_moins_2ans",
}[value] || value || "inconnu");
const localisationValue = (value: string) => ({
  "tête/crochet": "tete_crochet",
  "corps-queue": "corps_queue",
}[value] || "inconnu");
const brcaValue = (value: string) => ({
  "muté": "mute",
  "non muté": "non_mute",
  "non testé": "non_teste",
}[value] || "non_teste");
const krasValue = (value: string) => ({
  "non testé": "non_teste",
  G12C: "g12c",
  G12D: "g12d",
  G12V: "g12v",
  autre: "autre_mute",
}[value] || value || "non_teste");
const msiValue = (value: string) => ({
  "non testé": "non_teste",
  positif: "msi_h",
  négatif: "mss",
}[value] || "non_teste");
const fusionValue = (value: string) => ({
  "non testé": "non_teste",
  oui: "positif",
  non: "negatif",
}[value] || "non_teste");

export function buildFullPatientPayload(data: any) {
  const bilirubine = numberOrNull(data.bilirubine);
  const lsn = Number(data.lsnBilirubine) || 21;
  return {
    nom: data.nom,
    prenom: data.prenom,
    date_naissance: data.dateNaissance || null,
    sexe: data.sexe || null,
    telephone: data.telephone || null,
    adresse: data.adresse || null,
    antecedents: [],
    mutations: [],
    evaluation: {
      date_evaluation: today(),
      contexte: "diagnostic",
      ecog: Number(data.ecog),
      etat_nutritionnel: nutritionValue(data.etatNutritionnel),
      douleur_presente: data.douleur === "présente",
      intensite_douleur: numberOrNull(data.intensiteDouleur),
      ictere: Boolean(data.ictere),
      diabete: diabetesValue(data.diabete),
      biologie: {
        ca19_9: numberOrNull(data.ca199),
        bilirubine,
        bilirubine_ratio_lsn: bilirubine == null ? null : bilirubine / lsn,
        cholestase: Boolean(data.cholestase),
        statut_dpd: dpdValue(data.statutDpd),
        albuminemie: numberOrNull(data.albuminemie),
      },
      imageries: [{
        type_imagerie: "TDM",
        date_imagerie: today(),
        localisation_tumorale: localisationValue(data.localisationTumorale),
        taille_tumorale_cm: numberOrNull(data.tailleTumorale),
        contact_ams: contactArteriel(data.contactAms),
        contact_tronc_coeliaque: contactArteriel(data.contactTroncCoeliaque),
        contact_art_hepatique: contactAhc(data.contactAhc),
        contact_vms_vp: contactVeineux(data.contactVmsVp),
        extension_ganglionnaire_regionale: Boolean(data.adenopathieRegionale),
        extension_ganglionnaire_distance: Boolean(data.adenopathieDistance),
        metastases_presentes: Boolean(data.metastases),
        metastases: [],
      }],
      histologie: {
        preuve_histologique: Boolean(data.preuveHistologique),
        statut_brca_germinal: brcaValue(data.statutBrca),
        statut_kras: krasValue(data.statutKras),
        statut_msi_dmmr: msiValue(data.statutMsiDmmr),
        fusion_ntrk: fusionValue(data.fusionNtrk),
        fusion_nrg1: fusionValue(data.fusionNrg1),
      },
      analyses: [],
      comorbidites: [],
    },
  };
}

export async function createPatientAndCalculate(data: any) {
  const created = await request<FullCreationResult>("/patients/full", {
    method: "POST",
    body: JSON.stringify(buildFullPatientPayload(data)),
  });
  const calculated = await request<ClinicalResult>(`/clinical-rules/evaluations/${created.id_evaluation}/calculate`, {
    method: "POST",
    body: JSON.stringify({
      categorie_t: data.categorieT,
      categorie_n: data.categorieN,
      categorie_m: data.categorieM || null,
      version_moteur: "tncd-2024-v1",
    }),
  });
  return { created, calculated };
}

export async function login(email: string, password: string) {
  const response = await request<{ access_token: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  window.localStorage.setItem("pancrea_access_token", response.access_token);
  return response;
}

export async function signup(payload: { nom: string; prenom: string; email: string; password: string; telephone?: string; hopital?: string }) {
  return request<{ user: string; medecin_id: number; need_email_confirmation: boolean }>("/auth/signup", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export { API_URL };
