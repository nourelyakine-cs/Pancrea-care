"use client";

import { useState, useEffect, use } from "react";
import Step1Demographie from "../../add/components/Step1Demographie";
import Step2EtatClinique from "../../add/components/Step2EtatClinique";
import Step3Biologie from "../../add/components/Step3Biologie";
import Step4Imagerie from "../../add/components/Step4Imagerie";
import Step5Tnm from "../../add/components/Step5Tnm";
import Step6Histologie from "../../add/components/Step6Histologie";
import Step7Parcours from "../../add/components/Step7Parcours";

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
  const resolvedParams = use(params);
  const patientId = resolvedParams.id;

  const [currentStep, setCurrentStep] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // État global initialisé vide
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

  // Chargement des données statiques au montage
  useEffect(() => {
    const loadedData = MOCK_PATIENTS_DATABASE[patientId];
    if (loadedData) {
      setPatientData(loadedData);
    }
    setIsLoading(false);
  }, [patientId]);

  const updateData = (fields: Partial<typeof patientData>) => {
    setPatientData((prev) => ({ ...prev, ...fields }));
  };

  const handleNextStep = (nextStep: number) => {
    setCurrentStep(nextStep);
  };

  const handleStepClick = (targetStep: number) => {
    setCurrentStep(targetStep);
  };

  const handleSubmitUpdate = () => {
    console.log("Données mises à jour pour le patient", patientId, ":", patientData);
    alert(`Fiche du patient ${patientData.nom} ${patientData.prenom} mise à jour avec succès !`);
  };

  if (isLoading) {
    return (
      <div className="p-8 text-center text-xs text-gray-500 font-serif">
        Chargement des données du patient...
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-serif">
      
      {/* EN-TÊTE D'ÉDITION */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-[10px] font-bold text-[#209BBF] bg-cyan-50 px-2 py-0.5 rounded-md">
            {patientId}
          </span>
          <h1 className="text-lg font-bold text-[#1F3D4D] mt-1">
            Modifier le dossier : {patientData.nom} {patientData.prenom}
          </h1>
        </div>
        <span className="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1 rounded-xl font-medium">
          Mode Édition
        </span>
      </div>

      {/* STEPPER INTERACTIF LIBRE */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between text-xs overflow-x-auto">
        {[
          { step: 1, label: "Démographie" },
          { step: 2, label: "Clinique" },
          { step: 3, label: "Biologie" },
          { step: 4, label: "Imagerie" },
          { step: 5, label: "TNM" },
          { step: 6, label: "Histologie" },
          { step: 7, label: "Parcours" },
        ].map((item, idx, arr) => {
          const isCurrent = currentStep === item.step;

          return (
            <div key={item.step} className="flex items-center flex-1 min-w-max">
              <button 
                type="button"
                onClick={() => handleStepClick(item.step)}
                className={`flex items-center gap-2 font-bold cursor-pointer transition ${
                  isCurrent ? 'text-[#1D7893]' : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-white transition ${
                  isCurrent ? 'bg-[#1D7893]' : 'bg-gray-300'
                }`}>
                  {item.step}
                </span>
                <span>{item.label}</span>
              </button>
              {idx < arr.length - 1 && <div className="h-[2px] bg-gray-200 flex-1 mx-2 min-w-[15px]" />}
            </div>
          );
        })}
      </div>

      {/* RENDU DES COMPOSANTS PRÉ-REMPLIS */}
      {currentStep === 1 && <Step1Demographie data={patientData} updateData={updateData} onNext={() => handleNextStep(2)} />}
      {currentStep === 2 && <Step2EtatClinique data={patientData} updateData={updateData} onNext={() => handleNextStep(3)} onPrev={() => setCurrentStep(1)} />}
      {currentStep === 3 && <Step3Biologie data={patientData} updateData={updateData} onNext={() => handleNextStep(4)} onPrev={() => setCurrentStep(2)} />}
      {currentStep === 4 && <Step4Imagerie data={patientData} updateData={updateData} onNext={() => handleNextStep(5)} onPrev={() => setCurrentStep(3)} />}
      {currentStep === 5 && <Step5Tnm data={patientData} updateData={updateData} onNext={() => handleNextStep(6)} onPrev={() => setCurrentStep(4)} />}
      {currentStep === 6 && <Step6Histologie data={patientData} updateData={updateData} onNext={() => handleNextStep(7)} onPrev={() => setCurrentStep(5)} />}
      {currentStep === 7 && <Step7Parcours data={patientData} updateData={updateData} onSubmitFinal={handleSubmitUpdate} onPrev={() => setCurrentStep(6)} />}

    </div>
  );
}