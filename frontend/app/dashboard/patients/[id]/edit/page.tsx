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

// Base de données statique fictive pour le pré-remplissage
const MOCK_PATIENTS_DATABASE: Record<string, any> = {
  "PAT-2026-001": {
    nom: "Benali",
    prenom: "Mohamed",
    telephone: "0550 12 34 56",
    adresse: "Alger, Bab El Oued",
    dateNaissance: "1964-03-14",
    sexe: "M",
    age: "62",
    ecog: 1,
    etatNutritionnel: "normal",
    comorbiditesLourdes: false,
    douleur: "présente",
    intensiteDouleur: "Modérée (4/10)",
    ictere: false,
    angiocholite: false,
    diabete: "absent",
    cholestase: false,
    patientNonOperable: false,
    ca199: "120",
    bilirubine: "15",
    lsnBilirubine: 17,
    statutDpd: "normal",
    albuminemie: "42",
    localisationTumorale: "tête/crochet",
    tailleTumorale: "2.5",
    contactAms: "pas de contact",
    contactTroncCoeliaque: "pas de contact",
    contactAhc: "pas de contact",
    contactVmsVp: "<180° sans irrégularité",
    adenopathieRegionale: true,
    adenopathieDistance: false,
    metastases: false,
    categorieT: "T2",
    categorieN: "N1",
    categorieM: "M0",
    preuveHistologique: true,
    statutBrca: "non muté",
    statutKras: "G12D",
    statutMsiDmmr: "négatif",
    fusionNtrk: "non testé",
    fusionNrg1: "non testé",
    ligneTraitementActuelle: 1,
    reponseTraitementEnCours: "stable",
    traitementsRecusTexte: "FOLFIRINOX",
    traitementsRecus: ["FOLFIRINOX"],
    lignePrecedente: "",
    dureeChimiotherapieMois: "5",
    tumeurControle: true,
    nouvellesMetastases: false,
    chirurgieDembleePrevue: false,
    traitementMedicalPrevu: true,
    pasDeProgressionApres16SemainesPlatine: true,
    toxiciteResiduelle: false,
    detailsToxicite: "",
  },
  "PAT-2026-002": {
    nom: "Khadraoui",
    prenom: "Amina",
    telephone: "0661 98 76 54",
    adresse: "Oran, Centre ville",
    dateNaissance: "1951-08-20",
    sexe: "F",
    age: "75",
    ecog: 2,
    etatNutritionnel: "dénutrition modérée",
    comorbiditesLourdes: true,
    douleur: "présente",
    intensiteDouleur: "Sévère (7/10)",
    ictere: true,
    angiocholite: false,
    diabete: "récent (<2 ans)",
    cholestase: true,
    patientNonOperable: true,
    ca199: "620",
    bilirubine: "48",
    lsnBilirubine: 21,
    statutDpd: "déficit partiel",
    albuminemie: "31",
    localisationTumorale: "corps/queue",
    tailleTumorale: "3.8",
    contactAms: ">=180°",
    contactTroncCoeliaque: "<180°",
    contactAhc: "court reconstructible",
    contactVmsVp: ">=180° ou irregularite ou occlusion reconstructible",
    adenopathieRegionale: true,
    adenopathieDistance: true,
    metastases: true,
    categorieT: "T4",
    categorieN: "N1",
    categorieM: "M1",
    preuveHistologique: true,
    statutBrca: "muté",
    statutKras: "G12C",
    statutMsiDmmr: "positif",
    fusionNtrk: "oui",
    fusionNrg1: "non",
    ligneTraitementActuelle: 2,
    reponseTraitementEnCours: "progression",
    traitementsRecusTexte: "Gemcitabine, FOLFIRINOX",
    traitementsRecus: ["Gemcitabine", "FOLFIRINOX"],
    lignePrecedente: "1",
    dureeChimiotherapieMois: "3",
    tumeurControle: false,
    nouvellesMetastases: true,
    chirurgieDembleePrevue: false,
    traitementMedicalPrevu: true,
    pasDeProgressionApres16SemainesPlatine: false,
    toxiciteResiduelle: true,
    detailsToxicite: "Neuropathie périphérique grade 2",
  },
};

export default function EditPatientPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const resolvedParams = use(params);
  const patientId = resolvedParams.id;

  const [currentStep, setCurrentStep] = useState<number>(1);
  const [maxReachedStep, setMaxReachedStep] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  // État global du patient
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

  // Chargement des données au montage
  useEffect(() => {
    const loadedData = MOCK_PATIENTS_DATABASE[patientId];
    if (loadedData) {
      setPatientData(loadedData);
      setMaxReachedStep(9);
    }
    setIsLoading(false);
  }, [patientId]);

  // Validations par étape
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

  const handleSubmitUpdate = () => {
    console.log("Mise à jour et nouvelle évaluation enregistrées pour :", patientId, patientData);
    
    // Déclenche l'écran de succès
    setIsSuccess(true);

    // Redirection après 2.5 secondes vers la liste des patients
    setTimeout(() => {
      router.push("/dashboard/patients");
    }, 2500);
  };

  if (isLoading) {
    return (
      <div className="p-8 text-center text-xs text-gray-500 font-serif">
        Chargement des données du patient...
      </div>
    );
  }

  // ÉCRAN DE SUCCÈS DESIGNÉ
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
          Mode Mise à jour
        </span>
      </div>

      {/* STEPPER INTERACTIF (9 ÉTAPES) */}
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

      {/* COMPOSANTS DE CHAQUE ÉTAPE (1 à 7) */}
      {currentStep === 1 && <Step1Demographie data={patientData} updateData={updateData} onNext={() => handleNextStep(2)} />}
      {currentStep === 2 && <Step2EtatClinique data={patientData} updateData={updateData} onNext={() => handleNextStep(3)} onPrev={() => setCurrentStep(1)} />}
      {currentStep === 3 && <Step3Biologie data={patientData} updateData={updateData} onNext={() => handleNextStep(4)} onPrev={() => setCurrentStep(2)} />}
      {currentStep === 4 && <Step4Imagerie data={patientData} updateData={updateData} onNext={() => handleNextStep(5)} onPrev={() => setCurrentStep(3)} />}
      {currentStep === 5 && <Step5Tnm data={patientData} updateData={updateData} onNext={() => handleNextStep(6)} onPrev={() => setCurrentStep(4)} />}
      {currentStep === 6 && <Step6Histologie data={patientData} updateData={updateData} onNext={() => handleNextStep(7)} onPrev={() => setCurrentStep(5)} />}
      {currentStep === 7 && <Step7Parcours data={patientData} updateData={updateData} onSubmitFinal={() => handleNextStep(8)} onPrev={() => setCurrentStep(6)} />}

      {/* ÉTAPE 8 : CALCULS */}
      {currentStep === 8 && <Step8Calcul onPrev={() => setCurrentStep(7)} onNext={() => handleNextStep(9)} />}

      {/* ÉTAPE 9 : NOUVELLE ÉVALUATION ET BOUTON DE SOUMISSION */}
      {currentStep === 9 && (
        <div className="space-y-6">
          <EvaluationPage patientId={patientId} data={patientData} />

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