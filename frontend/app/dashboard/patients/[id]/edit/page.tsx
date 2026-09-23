"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import Step1Demographie from "../../add/components/Step1Demographie";
import Step2EtatClinique from "../../add/components/Step2EtatClinique";
import Step3Biologie from "../../add/components/Step3Biologie";
import Step4Imagerie from "../../add/components/Step4Imagerie";
import Step5Tnm from "../../add/components/Step5Tnm";
import Step6Histologie from "../../add/components/Step6Histologie";
import Step7Parcours from "../../add/components/Step7Parcours";
import Step8Calcul from "../../add/components/Step8Calcul";
import EvaluationPage from "../../../evaluation/page";

import { CheckCircle2, ArrowLeft, Loader2, Sparkles, FileText } from "lucide-react";
import {
  createEvaluationAndCalculate,
  getPatient,
  getPatientEvaluations,
  getDossierDetail,
  updatePatient,
  type ClinicalResult,
  type DossierDetail,
  type DetailEvaluation,
  type EvaluationResume,
} from "@/lib/api";

const initialData = {
  nom: "", prenom: "", dateNaissance: "", sexe: "", telephone: "", adresse: "", age: "", ecog: 0, etatNutritionnel: "normal", comorbiditesLourdes: false, douleur: "absente", intensiteDouleur: "", ictere: false, angiocholite: false, diabete: "absent", cholestase: false, patientNonOperable: false, ca199: "", bilirubine: "", lsnBilirubine: 21, statutDpd: "normal", albuminemie: "", localisationTumorale: "tête/crochet", tailleTumorale: "", contactAms: "pas de contact", contactTroncCoeliaque: "pas de contact", contactAhc: "pas de contact", contactVmsVp: "<180° sans irrégularité", adenopathieRegionale: false, adenopathieDistance: false, metastases: false, categorieT: "T1a", categorieN: "N0", categorieM: "M0", preuveHistologique: false, statutBrca: "non testé", statutKras: "non testé", statutMsiDmmr: "non testé", fusionNtrk: "non testé", fusionNrg1: "non testé", ligneTraitementActuelle: 1, reponseTraitementEnCours: "stable", traitementsRecusTexte: "", traitementsRecus: [], lignePrecedente: "", dureeChimiotherapieMois: "", tumeurControle: false, nouvellesMetastases: false, chirurgieDembleePrevue: false, traitementMedicalPrevu: false, pasDeProgressionApres16SemainesPlatine: false, toxiciteResiduelle: false, detailsToxicite: "",
};

// Valeurs backend (snake_case) -> options des formulaires (camelCase FR)
const FORM_FROM_ENUM: Record<string, Record<string, string>> = {
  etatNutritionnel: { "denutrition_moderee": "dénutrition modérée", "denutrition_severe": "dénutrition sévère", "normal": "normal" },
  diabete: { "recent_moins_2ans": "récent (<2 ans)", "ancien": "ancien", "absent": "absent" },
  statutDpd: { "deficit_partiel": "déficit partiel", "deficit_complet": "déficit complet", "normal": "normal" },
  localisationTumorale: { "tete_crochet": "tête/crochet", "corps_queue": "corps-queue" },
  contactAms: { "absent": "pas de contact", "lt180": "<180°", "ge180": "≥180°" },
  contactTroncCoeliaque: { "absent": "pas de contact", "lt180": "<180°", "ge180": "≥180°" },
  contactAhc: { "absent": "pas de contact", "court_sans_envahissement": "court reconstructible", "envahissant": "non reconstructible" },
  contactVmsVp: {
    "lt180_sans_irregularite": "<180° sans irrégularité",
    "ge180_ou_irregularite": "≥180° ou irrégularité ou occlusion reconstructible",
    "occlusion_non_reconstructible": "occlusion non reconstructible",
  },
  statutBrca: { "mute": "muté", "non_mute": "non muté" },
  statutKras: { "g12c": "G12C", "g12d": "G12D", "g12v": "G12V", "autre_mute": "autre", "sauvage": "sauvage" },
  statutMsiDmmr: { "msi_h": "positif", "mss": "négatif" },
  fusionNtrk: { "positif": "oui", "negatif": "non" },
  fusionNrg1: { "positif": "oui", "negatif": "non" },
};

function fromEnum(key: string, value: string | null | undefined): string | undefined {
  if (!value) return undefined;
  return FORM_FROM_ENUM[key]?.[value] ?? value;
}

function lastEvaluation(detail: DossierDetail | null): DetailEvaluation | null {
  const evals = detail?.evaluations ?? [];
  return evals.length > 0 ? evals[evals.length - 1] : null;
}

function buildPrefill(
  detail: DossierDetail | null,
  resume: EvaluationResume | null,
): Partial<typeof initialData> {
  const patient = detail?.patient;
  const ev = lastEvaluation(detail);
  const bio = ev?.biologie;
  const histo = ev?.histologie;
  const img = ev?.imageries?.[0];

  return {
    nom: patient?.nom ?? "",
    prenom: patient?.prenom ?? "",
    dateNaissance: patient?.date_naissance ?? "",
    sexe: patient?.sexe ?? "",
    telephone: patient?.telephone ?? "",
    adresse: patient?.adresse ?? "",
    age: "",
    ecog: ev?.ecog ?? 0,
    etatNutritionnel: fromEnum("etatNutritionnel", ev?.etat_nutritionnel) ?? "normal",
    douleur: ev?.douleur_presente === true ? "présente" : ev?.douleur_presente === false ? "absente" : "absente",
    intensiteDouleur: ev?.intensite_douleur != null ? String(ev.intensite_douleur) : "",
    ictere: ev?.ictere ?? false,
    diabete: fromEnum("diabete", ev?.diabete) ?? "absent",
    cholestase: bio?.cholestase ?? false,
    ca199: bio?.ca19_9 != null ? String(bio.ca19_9) : "",
    bilirubine: bio?.bilirubine != null ? String(bio.bilirubine) : "",
    statutDpd: fromEnum("statutDpd", bio?.statut_dpd) ?? "normal",
    albuminemie: bio?.albuminemie != null ? String(bio.albuminemie) : "",
    localisationTumorale: fromEnum("localisationTumorale", img?.localisation_tumorale) ?? "tête/crochet",
    tailleTumorale: img?.taille_tumorale_cm != null ? String(img.taille_tumorale_cm) : "",
    contactAms: fromEnum("contactAms", img?.contact_ams) ?? "pas de contact",
    contactTroncCoeliaque: fromEnum("contactTroncCoeliaque", img?.contact_tronc_coeliaque) ?? "pas de contact",
    contactAhc: fromEnum("contactAhc", img?.contact_art_hepatique) ?? "pas de contact",
    contactVmsVp: fromEnum("contactVmsVp", img?.contact_vms_vp) ?? "<180° sans irrégularité",
    adenopathieRegionale: img?.extension_ganglionnaire_regionale ?? false,
    adenopathieDistance: img?.extension_ganglionnaire_distance ?? false,
    metastases: img?.metastases_presentes ?? false,
    categorieT: resume?.categorie_t ?? "T1a",
    categorieN: resume?.categorie_n ?? "N0",
    categorieM: resume?.categorie_m ?? "M0",
    preuveHistologique: histo?.preuve_histologique ?? false,
    statutBrca: fromEnum("statutBrca", histo?.statut_brca_germinal) ?? "non testé",
    statutKras: fromEnum("statutKras", histo?.statut_kras) ?? "non testé",
    statutMsiDmmr: fromEnum("statutMsiDmmr", histo?.statut_msi_dmmr) ?? "non testé",
    fusionNtrk: fromEnum("fusionNtrk", histo?.fusion_ntrk) ?? "non testé",
    fusionNrg1: fromEnum("fusionNrg1", histo?.fusion_nrg1) ?? "non testé",
    traitementsRecusTexte: "",
    traitementsRecus: [],
    lignePrecedente: "",
  };
}

export default function EditPatientPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const resolvedParams = use(params);
  const patientId = resolvedParams.id;

  const [currentStep, setCurrentStep] = useState<number>(1);
  const [maxReachedStep, setMaxReachedStep] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [prefillError, setPrefillError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const [patientData, setPatientData] = useState(initialData);
  const [calculation, setCalculation] = useState<ClinicalResult | null>(null);
  const [createdIds, setCreatedIds] = useState<{ id_patient: number; id_evaluation: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Chargement du patient réel + de sa dernière évaluation pour pré-remplir
  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setPrefillError(null);
    (async () => {
      try {
        const resume = await getPatientEvaluations(patientId);
        if (!active) return;
        const latest = resume && resume.length > 0 ? resume[0] : null;
        setPatientData((prev) => ({ ...prev, ...buildPrefill(null, latest) }));

        if (latest?.id_dossier) {
          const detail = await getDossierDetail(latest.id_dossier);
          if (active) setPatientData((prev) => ({ ...prev, ...buildPrefill(detail, latest) }));
        } else {
          const patient = await getPatient(patientId);
          if (active) {
            setPatientData((prev) => ({
              ...prev,
              nom: patient.nom,
              prenom: patient.prenom,
              dateNaissance: patient.date_naissance ?? "",
              sexe: patient.sexe ?? "",
              telephone: patient.telephone ?? "",
              adresse: patient.adresse ?? "",
            }));
          }
        }
      } catch (cause) {
        if (!active) return;
        setPrefillError(
          typeof cause === "object" && cause !== null && "detail" in cause
            ? String((cause as { detail: unknown }).detail)
            : "Impossible de charger les données du patient.",
        );
      } finally {
        if (active) setIsLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [patientId]);

  // Validations par étape
  const validity = [
    true,
    Boolean(patientData.nom.trim() && patientData.prenom.trim() && patientData.sexe && patientData.dateNaissance),
    Boolean(patientData.etatNutritionnel && patientData.douleur),
    Boolean(patientData.ca199 !== "" && patientData.bilirubine !== ""),
    Boolean(patientData.localisationTumorale && patientData.tailleTumorale !== ""),
    Boolean(patientData.categorieT && patientData.categorieN && patientData.categorieM),
    true,
    Boolean(patientData.ligneTraitementActuelle && patientData.reponseTraitementEnCours),
  ];
  const isStepValid = (step: number) => validity[step - 1] ?? true;
  const canAccessStep = (step: number) => step === 1 || Array.from({ length: step - 1 }, (_, i) => i + 1).every(isStepValid);
  const updateData = (fields: Partial<typeof initialData>) => setPatientData((prev) => ({ ...prev, ...fields }));

  const handleNextStep = async (nextStep: number) => {
    if (!isStepValid(currentStep) && nextStep > currentStep) {
      alert("Veuillez remplir correctement tous les champs obligatoires de cette étape avant de continuer.");
      return;
    }

    if (nextStep === 8) {
      setCurrentStep(8);
      setMaxReachedStep(8);
      setLoading(true);
      setError(null);
      try {
        // Identique à la page « Nouveau patient » : une seule création
        // d'évaluation + calcul, sans appel intermédiaire bloquant.
        const response = await createEvaluationAndCalculate(patientId, patientData);
        setCalculation(response.calculated);
        setCreatedIds({ id_patient: response.created.id_patient, id_evaluation: response.created.id_evaluation });
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : "Erreur inconnue lors de l'intégration backend.");
      } finally {
        setLoading(false);
      }
      return;
    }

    setCurrentStep(nextStep);
    setMaxReachedStep((old) => Math.max(old, nextStep));
  };

  const handleStepClick = (targetStep: number) => {
    if (targetStep <= 8) {
      if (!canAccessStep(targetStep)) {
        alert("Vous devez d'abord compléter toutes les étapes précédentes.");
        return;
      }
    } else if (targetStep > maxReachedStep) {
      return;
    }
    setCurrentStep(targetStep);
  };

  const handleSubmitUpdate = () => {
    updatePatient(patientId, {
      nom: patientData.nom,
      prenom: patientData.prenom,
      date_naissance: patientData.dateNaissance || null,
      sexe: patientData.sexe || null,
      telephone: patientData.telephone || null,
      adresse: patientData.adresse || null,
    }).catch(() => {
      /* la mise à jour d'identité est best-effort : l'évaluation est déjà enregistrée */
    });
    setIsSuccess(true);
    setTimeout(() => {
      router.push("/dashboard/patients");
    }, 2500);
  };

  if (isLoading) {
    return (
      <div className="p-10 text-center font-serif">
        <Loader2 className="w-6 h-6 animate-spin text-[#1D7893] mx-auto mb-3" />
        <p className="text-xs text-gray-500">Chargement des données du patient et de sa dernière évaluation...</p>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center font-serif p-4">
        <div className="bg-white p-8 rounded-3xl border border-emerald-100 shadow-xl text-center max-w-md w-full space-y-6 transform animate-in fade-in zoom-in duration-300">
          <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
            <CheckCircle2 className="w-10 h-10" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-[#1F3D4D]">Mise à jour réussie !</h2>
            <p className="text-xs text-gray-500">
              Patient <span className="font-semibold text-gray-800">{patientData.nom} {patientData.prenom}</span> ({patientId})
            </p>
          </div>
          <div className="bg-emerald-50/60 border border-emerald-100 rounded-2xl p-4 space-y-2 text-left text-xs">
            <div className="flex items-center gap-2 text-emerald-800 font-semibold">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>Informations du patient mises à jour</span>
            </div>
            <div className="flex items-center gap-2 text-emerald-800 font-semibold">
              <FileText className="w-4 h-4 text-emerald-600" />
              <span>Nouvelle évaluation CDSS sauvegardée</span>
            </div>
          </div>
          <div className="pt-2 flex items-center justify-center gap-2 text-xs text-gray-400">
            <Loader2 className="w-4 h-4 animate-spin text-[#1D7893]" />
            <span>Redirection vers la liste des patients...</span>
          </div>
        </div>
      </div>
    );
  }

  const steps = ["Démographie", "Clinique", "Biologie", "Imagerie", "TNM", "Histologie", "Parcours", "Calculs CDSS", "Évaluation"];

  return (
    <div className="max-w-5xl mx-auto space-y-6 font-serif">
      {/* EN-TÊTE D'ÉDITION */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-[10px] font-bold text-[#209BBF] bg-cyan-50 px-2 py-0.5 rounded-md">
            {patientId}
          </span>
          <h1 className="text-lg font-bold text-[#1F3D4D] mt-1">
            Éditer & Évaluer : {patientData.nom} {patientData.prenom}
          </h1>
        </div>
        <span className="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1 rounded-xl font-medium">
          Mode Mise à jour — Nouvelle évaluation
        </span>
      </div>

      {prefillError && (
        <div className="bg-amber-50 border border-amber-200 text-amber-800 text-xs rounded-2xl px-4 py-3">
          Données d'origine indisponibles ({prefillError}). Le formulaire est pré-rempli par défaut — vous pouvez tout de même saisir une nouvelle évaluation.
        </div>
      )}

      {/* STEPPER INTERACTIF (9 ÉTAPES) */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between text-xs overflow-x-auto">
        {steps.map((label, index) => {
          const step = index + 1;
          const completed = isStepValid(step) && maxReachedStep > step;
          const accessible = step <= 7 ? canAccessStep(step) : step <= maxReachedStep;
          return (
            <div key={step} className="flex items-center flex-1 min-w-max">
              <button
                type="button"
                onClick={() => handleStepClick(step)}
                disabled={!accessible}
                className={`flex items-center gap-2 font-bold transition ${!accessible ? "cursor-not-allowed opacity-40" : "cursor-pointer"} ${currentStep === step ? "text-[#1D7893]" : "text-gray-400"}`}
              >
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-white ${currentStep === step ? "bg-[#1D7893]" : completed ? "bg-emerald-500" : "bg-gray-300"}`}>
                  {completed ? "✓" : step}
                </span>
                <span>{label}</span>
              </button>
              {step < steps.length && <div className="h-[2px] bg-gray-200 flex-1 mx-2 min-w-[15px]" />}
            </div>
          );
        })}
      </div>

      {/* COMPOSANTS DE CHAQUE ÉTAPE (1 à 7) */}
      {currentStep === 1 && <Step1Demographie data={patientData} updateData={updateData} onNext={() => handleNextStep(2)} />}
      {currentStep === 2 && <Step2EtatClinique data={patientData} updateData={updateData} onNext={() => handleNextStep(3)} onPrev={() => setCurrentStep(1)} />}
      {currentStep === 3 && <Step3Biologie data={patientData} updateData={updateData} onNext={() => handleNextStep(4)} onPrev={() => setCurrentStep(2)} />}
      {currentStep === 4 && <Step4Imagerie data={patientData} updateData={updateData} onNext={() => handleNextStep(5)} onPrev={() => setCurrentStep(3)} />}
      {currentStep === 5 && <Step5Tnm data={patientData} updateData={updateData} onNext={() => handleNextStep(6)} onPrev={() => setCurrentStep(4)} />}
      {currentStep === 6 && <Step6Histologie data={patientData} updateData={updateData} onNext={() => handleNextStep(7)} onPrev={() => setCurrentStep(5)} />}
      {currentStep === 7 && <Step7Parcours data={patientData} updateData={updateData} submitting={loading} error={error} onSubmitFinal={() => handleNextStep(8)} onPrev={() => setCurrentStep(6)} />}

      {/* ÉTAPE 8 : CALCULS */}
      {currentStep === 8 && <Step8Calcul result={calculation} loading={loading} error={error} onPrev={() => setCurrentStep(7)} onNext={() => handleNextStep(9)} />}

      {/* ÉTAPE 9 : RAPPORT D'ÉVALUATION ET SAUVEGARDE */}
      {currentStep === 9 && (
        <div className="space-y-6">
          <EvaluationPage
            patientId={createdIds ? `PAT-${createdIds.id_patient}` : patientId}
            idEvaluation={createdIds?.id_evaluation || null}
            data={patientData}
          />
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex justify-between items-center">
            <button
              type="button"
              onClick={() => setCurrentStep(8)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50 transition"
            >
              <ArrowLeft className="w-4 h-4" /> Modifier les Calculs
            </button>
            <button
              type="button"
              onClick={handleSubmitUpdate}
              className="flex items-center gap-2 px-8 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-lg transition-all"
            >
              <CheckCircle2 className="w-5 h-5" /> Enregistrer et Sauvegarder l'Évaluation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}