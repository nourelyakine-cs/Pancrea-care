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

export default function AddPatientPage() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [maxReachedStep, setMaxReachedStep] = useState<number>(1);

  // État global complet
  const [patientData, setPatientData] = useState({
    nom: "", prenom: "", dateNaissance: "", sexe: "", telephone: "", adresse: "", age: "",
    ecog: 0, etatNutritionnel: "normal", comorbiditesLourdes: false, douleur: "absente",
    intensiteDouleur: "", ictere: false, angiocholite: false, diabete: "absent", cholestase: false,
    patientNonOperable: false,
    ca199: "", bilirubine: "", lsnBilirubine: 21, statutDpd: "normal", albuminemie: "",
    localisationTumorale: "tête/crochet", tailleTumorale: "", contactAms: "pas de contact",
    contactTroncCoeliaque: "pas de contact", contactAhc: "pas de contact",
    contactVmsVp: "<180° sans irrégularité", adenopathieRegionale: false,
    adenopathieDistance: false, metastases: false,
    categorieT: "T1a", categorieN: "N0", categorieM: "M0",
    preuveHistologique: false, statutBrca: "non testé", statutKras: "non testé",
    statutMsiDmmr: "non testé", fusionNtrk: "non testé", fusionNrg1: "non testé",
    ligneTraitementActuelle: 1, reponseTraitementEnCours: "stable", traitementsRecusTexte: "",
    traitementsRecus: [], lignePrecedente: "", dureeChimiotherapieMois: "",
    tumeurControle: false, nouvellesMetastases: false, chirurgieDembleePrevue: false,
    traitementMedicalPrevu: false, pasDeProgressionApres16SemainesPlatine: false,
    toxiciteResiduelle: false, detailsToxicite: "",
  });

  const isStep1Valid = Boolean(patientData.nom.trim() && patientData.prenom.trim() && patientData.sexe && patientData.dateNaissance);
  const isStep2Valid = Boolean(patientData.etatNutritionnel && patientData.douleur);
  const isStep3Valid = Boolean(patientData.ca199 !== "" && patientData.bilirubine !== "");
  const isStep4Valid = Boolean(patientData.localisationTumorale && patientData.tailleTumorale !== "");
  const isStep5Valid = Boolean(patientData.categorieT && patientData.categorieN && patientData.categorieM);
  const isStep6Valid = true;
  const isStep7Valid = Boolean(patientData.ligneTraitementActuelle && patientData.reponseTraitementEnCours);

  const isStepValid = (stepNumber: number): boolean => {
    switch (stepNumber) {
      case 1: return isStep1Valid;
      case 2: return isStep2Valid;
      case 3: return isStep3Valid;
      case 4: return isStep4Valid;
      case 5: return isStep5Valid;
      case 6: return isStep6Valid;
      case 7: return isStep7Valid;
      default: return true;
    }
  };

  const canAccessStep = (targetStep: number): boolean => {
    if (targetStep === 1) return true;
    for (let i = 1; i < targetStep; i++) {
      if (!isStepValid(i)) return false;
    }
    return true;
  };

  const updateData = (fields: Partial<typeof patientData>) => {
    setPatientData((prev) => ({ ...prev, ...fields }));
  };

  const handleNextStep = (nextStep: number) => {
    if (!isStepValid(currentStep)) {
      alert("Veuillez remplir correctement tous les champs obligatoires de cette étape avant de continuer.");
      return;
    }
    setCurrentStep(nextStep);
    if (nextStep > maxReachedStep) {
      setMaxReachedStep(nextStep);
    }
  };

  const handleStepClick = (targetStep: number) => {
    if (!canAccessStep(targetStep)) {
      alert("Vous devez d'abord compléter toutes les étapes précédentes.");
      return;
    }
    setCurrentStep(targetStep);
  };

  const handleSubmitFinal = () => {
    console.log("Dossier patient et calculs enregistrés avec succès :", patientData);
    alert("Le patient et son évaluation ont été enregistrés avec succès !");
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 font-serif">
      {/* STEPPER INTERACTIF */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between text-xs overflow-x-auto">
        {[
          { step: 1, label: "Démographie" },
          { step: 2, label: "Clinique" },
          { step: 3, label: "Biologie" },
          { step: 4, label: "Imagerie" },
          { step: 5, label: "TNM" },
          { step: 6, label: "Histologie" },
          { step: 7, label: "Parcours" },
          { step: 8, label: "Calculs CDSS" },
          { step: 9, label: "Évaluation" },
        ].map((item, idx, arr) => {
          const isCompleted = isStepValid(item.step) && maxReachedStep > item.step;
          const isCurrent = currentStep === item.step;
          const isNavigable = canAccessStep(item.step);

          return (
            <div key={item.step} className="flex items-center flex-1 min-w-max">
              <button 
                type="button"
                onClick={() => handleStepClick(item.step)}
                disabled={!isNavigable}
                className={`flex items-center gap-2 font-bold transition ${
                  !isNavigable ? 'cursor-not-allowed opacity-40' : 'cursor-pointer'
                } ${isCurrent ? 'text-[#1D7893]' : 'text-gray-400'}`}
              >
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-white ${
                  isCurrent 
                    ? 'bg-[#1D7893]' 
                    : isCompleted 
                    ? 'bg-emerald-500' 
                    : 'bg-gray-300'
                }`}>
                  {isCompleted ? "✓" : item.step}
                </span>
                <span>{item.label}</span>
              </button>
              {idx < arr.length - 1 && <div className="h-[2px] bg-gray-200 flex-1 mx-2 min-w-[15px]" />}
            </div>
          );
        })}
      </div>

      {/* COMPOSANTS DE CHAQUE ÉTAPE */}
      {currentStep === 1 && <Step1Demographie data={patientData} updateData={updateData} onNext={() => handleNextStep(2)} />}
      {currentStep === 2 && <Step2EtatClinique data={patientData} updateData={updateData} onNext={() => handleNextStep(3)} onPrev={() => setCurrentStep(1)} />}
      {currentStep === 3 && <Step3Biologie data={patientData} updateData={updateData} onNext={() => handleNextStep(4)} onPrev={() => setCurrentStep(2)} />}
      {currentStep === 4 && <Step4Imagerie data={patientData} updateData={updateData} onNext={() => handleNextStep(5)} onPrev={() => setCurrentStep(3)} />}
      {currentStep === 5 && <Step5Tnm data={patientData} updateData={updateData} onNext={() => handleNextStep(6)} onPrev={() => setCurrentStep(4)} />}
      {currentStep === 6 && <Step6Histologie data={patientData} updateData={updateData} onNext={() => handleNextStep(7)} onPrev={() => setCurrentStep(5)} />}
      {currentStep === 7 && <Step7Parcours data={patientData} updateData={updateData} onSubmitFinal={() => handleNextStep(8)} onPrev={() => setCurrentStep(6)} />}
      
      {/* ÉTAPE 8 ISOLÉE */}
      {currentStep === 8 && <Step8Calcul onPrev={() => setCurrentStep(7)} onNext={() => handleNextStep(9)} />}

      {/* ÉTAPE 9 : ÉVALUATION ET BOUTON FINAL */}
      {currentStep === 9 && (
        <div className="space-y-6">
          <EvaluationPage />

          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex justify-between items-center">
            <button
              type="button"
              onClick={() => setCurrentStep(8)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50"
            >
              <ArrowLeft className="w-4 h-4" /> Modifier les Calculs
            </button>
            <button
              type="button"
              onClick={handleSubmitFinal}
              className="flex items-center gap-2 px-8 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-lg transition-all"
            >
              <CheckCircle2 className="w-5 h-5" /> Enregistrer Définitivement le Patient
            </button>
          </div>
        </div>
      )}
    </div>
  );
}