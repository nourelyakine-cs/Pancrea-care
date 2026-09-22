"use client";

import { useState } from "react";
import Step1Demographie from "./components/Step1Demographie";
import Step2EtatClinique from "./components/Step2EtatClinique";
import Step3Biologie from "./components/Step3Biologie";
import Step4Imagerie from "./components/Step4Imagerie";
import Step5Tnm from "./components/Step5Tnm";
import Step6Histologie from "./components/Step6Histologie";
import Step7Parcours from "./components/Step7Parcours";
import Step8Calcul from "./components/Step8Calcul";
import EvaluationPage from "../../evaluation/page";
import { CheckCircle2, ArrowLeft } from "lucide-react";
import { createPatientAndCalculate, type ClinicalResult } from "../../../../lib/api";

const initialData = {
  nom: "", prenom: "", dateNaissance: "", sexe: "", telephone: "", adresse: "", age: "", ecog: 0, etatNutritionnel: "normal", comorbiditesLourdes: false, douleur: "absente", intensiteDouleur: "", ictere: false, angiocholite: false, diabete: "absent", cholestase: false, patientNonOperable: false, ca199: "", bilirubine: "", lsnBilirubine: 21, statutDpd: "normal", albuminemie: "", localisationTumorale: "tête/crochet", tailleTumorale: "", contactAms: "pas de contact", contactTroncCoeliaque: "pas de contact", contactAhc: "pas de contact", contactVmsVp: "<180° sans irrégularité", adenopathieRegionale: false, adenopathieDistance: false, metastases: false, categorieT: "T1a", categorieN: "N0", categorieM: "M0", preuveHistologique: false, statutBrca: "non testé", statutKras: "non testé", statutMsiDmmr: "non testé", fusionNtrk: "non testé", fusionNrg1: "non testé", ligneTraitementActuelle: 1, reponseTraitementEnCours: "stable", traitementsRecusTexte: "", traitementsRecus: [], lignePrecedente: "", dureeChimiotherapieMois: "", tumeurControle: false, nouvellesMetastases: false, chirurgieDembleePrevue: false, traitementMedicalPrevu: false, pasDeProgressionApres16SemainesPlatine: false, toxiciteResiduelle: false, detailsToxicite: "",
};

export default function AddPatientPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [maxReachedStep, setMaxReachedStep] = useState(1);
  const [patientData, setPatientData] = useState(initialData);
  const [calculation, setCalculation] = useState<ClinicalResult | null>(null);
  const [createdIds, setCreatedIds] = useState<{ id_patient: number; id_evaluation: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      alert("Veuillez remplir correctement tous les champs obligatoires avant de continuer."); 
      return; 
    }

    if (nextStep === 8) {
      setCurrentStep(8);
      setMaxReachedStep(8);
      setLoading(true);
      setError(null);
      try {
        const response = await createPatientAndCalculate(patientData);
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

  const handleFinal = () => { 
    if (!createdIds) return; 
    alert(`Patient enregistré avec succès ! ID patient : ${createdIds.id_patient}`); 
  };

  const steps = ["Démographie", "Clinique", "Biologie", "Imagerie", "TNM", "Histologie", "Parcours", "Calculs CDSS", "Évaluation"];

  return (
    <div className="max-w-5xl mx-auto space-y-6 font-serif">
      {/* STEPS HEADER */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between text-xs overflow-x-auto">
        {steps.map((label, index) => { 
          const step = index + 1; 
          const completed = isStepValid(step) && maxReachedStep > step; 
          const accessible = step <= 7 ? canAccessStep(step) : step <= maxReachedStep; 
          return (
            <div key={step} className="flex items-center flex-1 min-w-max">
              <button 
                type="button" 
                onClick={() => accessible && setCurrentStep(step)} 
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

      {/* FORM STEPS */}
      {currentStep === 1 && <Step1Demographie data={patientData} updateData={updateData} onNext={() => handleNextStep(2)} />}
      {currentStep === 2 && <Step2EtatClinique data={patientData} updateData={updateData} onNext={() => handleNextStep(3)} onPrev={() => setCurrentStep(1)} />}
      {currentStep === 3 && <Step3Biologie data={patientData} updateData={updateData} onNext={() => handleNextStep(4)} onPrev={() => setCurrentStep(2)} />}
      {currentStep === 4 && <Step4Imagerie data={patientData} updateData={updateData} onNext={() => handleNextStep(5)} onPrev={() => setCurrentStep(3)} />}
      {currentStep === 5 && <Step5Tnm data={patientData} updateData={updateData} onNext={() => handleNextStep(6)} onPrev={() => setCurrentStep(4)} />}
      {currentStep === 6 && <Step6Histologie data={patientData} updateData={updateData} onNext={() => handleNextStep(7)} onPrev={() => setCurrentStep(5)} />}
      {currentStep === 7 && <Step7Parcours data={patientData} updateData={updateData} submitting={loading} error={error} onSubmitFinal={() => handleNextStep(8)} onPrev={() => setCurrentStep(6)} />}
      {currentStep === 8 && <Step8Calcul result={calculation} loading={loading} error={error} onPrev={() => setCurrentStep(7)} onNext={() => handleNextStep(9)} />}
      
      {/* STEP 9: EVALUATION & REPORT */}
      {currentStep === 9 && (
        <div className="space-y-6">
          <EvaluationPage 
            patientId={createdIds ? `PAT-${createdIds.id_patient}` : "PAT-NEW"} 
            idEvaluation={createdIds?.id_evaluation || null} 
            data={patientData} 
          />
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex justify-between items-center">
            <button 
              type="button" 
              onClick={() => setCurrentStep(8)} 
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50 transition"
            >
              <ArrowLeft className="w-4 h-4" /> Modifier les calculs
            </button>
            <button 
              type="button" 
              onClick={handleFinal} 
              disabled={!createdIds} 
              className="flex items-center gap-2 px-8 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-xs font-bold shadow-lg transition"
            >
              <CheckCircle2 className="w-5 h-5" /> Enregistrer définitivement
            </button>
          </div>
        </div>
      )}
    </div>
  );
}