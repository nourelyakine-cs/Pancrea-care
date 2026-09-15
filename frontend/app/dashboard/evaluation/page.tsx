"use client";

import { use } from "react";
import { 
  CheckCircle2, 
  AlertCircle, 
  Activity, 
  ShieldCheck,
  Stethoscope,
  AlertTriangle,
  FileCheck
} from "lucide-react";

interface EvaluationPageProps {
  params?: Promise<{ id?: string }>;
  patientId?: string;
  data?: any;
}

export default function EvaluationPage({ params, patientId: propPatientId, data }: EvaluationPageProps) {
  // Gestion sécurisée de params : résolution uniquement s'il est fourni par Next.js
  const resolvedParams = params ? use(params) : null;
  const currentPatientId = propPatientId || resolvedParams?.id || "PAT-UNKNOWN";

  // Structure JSON 100% conforme au retour des endpoints /recommendations et /decisions du Backend
  const evaluationData = {
    id_decision: 3,
    id_evaluation: 19,
    date_decision: "2026-09-07T13:03:53.499Z",
    source_code: "TNCD-2024",
    source_version: "17/05/2024",
    necessite_rcp: true, // Automatique si Grade B ou accord d'experts
    
    // 1. Facts construits par le Backend
    facts: {
      age: data?.age ? Number(data.age) : 66,
      ecog: data?.ecog ?? 1,
      ca19_9: data?.ca199 ? Number(data.ca199) : 620,
      ictere: data?.ictere ?? true,
      bilirubine: data?.bilirubine ? Number(data.bilirubine) : 45,
      cholestase: data?.cholestase ?? true,
      metastases: data?.metastases ?? false,
      resecabilite: "resecable",
      stade_global: "IB",
      categorie_t: data?.categorieT || "T2",
      categorie_n: data?.categorieN || "N0",
      categorie_m: data?.categorieM || "M0",
      adenopathie_distance: false,
      statut_dpd: data?.statutDpd || "normal",
      critere_abc_b: true,
      critere_abc_c: false,
      type_abc: "AB"
    },

    // 2. Tableau dynamique de recommandations généré par le moteur (generate_recommendations)
    recommendations: [
      {
        code: "R02",
        titre: "Recommandation Néoadjuvante (Critère ABC Positif)",
        conclusion: "Résécable mais présence du critère ABC B (CA19-9 > 500 U/mL) : Discuter une chimiothérapie néoadjuvante en RCP avant toute chirurgie d'emblée.",
        reference: "TNCD 9.4.1.2",
        grade: "Grade B",
        criteres_evalues: {
          resecabilite: "resecable",
          critere_abc_b: true,
          ca19_9: data?.ca199 ? Number(data.ca199) : 620
        }
      },
      {
        code: "T1",
        titre: "Gestion de la Cholestase / Ictère",
        conclusion: "Ictère rétentionnel présent avec bilirubine à 45 µmol/L : Recommandation de drainage biliaire avant d'initier le traitement médical.",
        reference: "TNCD 9.2.1",
        grade: "Accord d'experts",
        criteres_evalues: {
          ictere: data?.ictere ?? true,
          bilirubine: data?.bilirubine ? Number(data.bilirubine) : 45
        }
      }
    ],

    // 3. Traçabilité (decision_path)
    regles_declenchees: ["R02", "T1"],
    decision_path: [
      { code: "R01", statut: "non_declenchee", nombre_conclusions: 0 },
      { code: "R02", statut: "declenchee", nombre_conclusions: 1 },
      { code: "T1", statut: "declenchee", nombre_conclusions: 1 },
      { code: "R03", statut: "ignoree", nombre_conclusions: 0 }
    ]
  };

  const { facts, recommendations, decision_path, necessite_rcp } = evaluationData;

  // Calcul du résumé des règles
  const totalRegles = decision_path.length;
  const reglesDeclencheesCount = decision_path.filter(r => r.statut === "declenchee").length;
  const reglesIgnoreesCount = decision_path.filter(r => r.statut === "ignoree").length;
  const reglesNonDeclencheesCount = decision_path.filter(r => r.statut === "non_declenchee").length;

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6 font-sans text-gray-800">
      
      {/* HEADER PAGE */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white p-5 rounded-2xl border border-gray-100 shadow-sm gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="bg-[#1D7893]/10 text-[#1D7893] text-xs font-bold px-2.5 py-1 rounded-md">
              Évaluation Décisionnelle CDSS
            </span>
            <span className="text-xs text-gray-400">
              Réf : {evaluationData.source_code} ({evaluationData.source_version}) — Patient : {currentPatientId}
            </span>
          </div>
          <h1 className="text-xl font-bold text-[#1F3D4D] mt-1">
            Rapport d'Aide à la Décision Clinique
          </h1>
        </div>
        
        <div className="flex items-center gap-4">
          {/* ALERTE RCP AUTOMATIQUE */}
          {necessite_rcp && (
            <div className="flex items-center gap-1.5 bg-amber-50 border border-amber-200 text-amber-800 px-3 py-1.5 rounded-xl text-xs font-bold">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Discussion RCP Requise</span>
            </div>
          )}
          <div className="text-right text-xs text-gray-500">
            <p>Évaluation N° : <span className="font-semibold text-gray-700">#{evaluationData.id_evaluation}</span></p>
            <p>Date : <span className="font-semibold text-gray-700">{new Date(evaluationData.date_decision).toLocaleDateString("fr-FR")}</span></p>
          </div>
        </div>
      </div>

      {/* SECTION 1 : RESUME CLINIQUE (FACTS) */}
      <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-[#1F3D4D] border-b pb-3">
          <Activity className="w-5 h-5 text-[#1D7893]" />
          <h2 className="font-bold text-sm uppercase tracking-wide">Résumé des Faits Patient (Facts Backend)</h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Stade TNM / Global</span>
            <span className="font-bold text-[#1F3D4D] text-sm">{facts.categorie_t}{facts.categorie_n}{facts.categorie_m} — Stade {facts.stade_global}</span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Résécabilité</span>
            <span className="font-bold text-emerald-600 text-sm capitalize">{facts.resecabilite}</span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Critères ABC</span>
            <span className="font-bold text-amber-700 text-sm">Type {facts.type_abc} (B: {facts.critere_abc_b ? "Oui" : "Non"})</span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Biologie Clé</span>
            <span className="font-bold text-[#1F3D4D] text-sm">CA19-9 : {facts.ca19_9} U/mL</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 text-xs pt-1">
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Âge: <b>{facts.age} ans</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">ECOG: <b>{facts.ecog}</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Métastases: <b>{facts.metastases ? "Oui" : "Non"}</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Ictère / Cholestase: <b>{facts.ictere ? "Oui" : "Non"}</b> (Bilirubine: {facts.bilirubine} µmol/L)</span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Statut DPD: <b>{facts.statut_dpd}</b></span>
        </div>
      </div>

      {/* SECTION 2 : RECOMMANDATIONS DYNAMIQUES DU CDSS */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 text-[#1F3D4D]">
          <Stethoscope className="w-5 h-5 text-[#1D7893]" />
          <h2 className="font-bold text-sm uppercase tracking-wide">
            Recommandations Générées ({recommendations.length})
          </h2>
        </div>

        {recommendations.map((rec, idx) => (
          <div key={idx} className="bg-white rounded-2xl border border-emerald-200 shadow-sm overflow-hidden">
            <div className="bg-emerald-50/70 p-4 border-b border-emerald-100 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <span className="bg-emerald-600 text-white font-bold text-xs px-2.5 py-1 rounded-lg">
                  {rec.code}
                </span>
                <div>
                  <h3 className="font-bold text-emerald-900 text-sm">{rec.titre}</h3>
                  <p className="text-xs text-emerald-700">Référence : {rec.reference}</p>
                </div>
              </div>
              <span className="bg-emerald-200/60 text-emerald-800 font-semibold text-xs px-2.5 py-1 rounded-full">
                {rec.grade}
              </span>
            </div>

            <div className="p-5 space-y-3">
              <div className="p-4 bg-emerald-50/30 border-l-4 border-emerald-500 text-gray-800 text-sm font-medium rounded-r-xl">
                {rec.conclusion}
              </div>

              {/* Critères ayant déclenché la règle */}
              <div className="pt-2">
                <span className="text-[11px] font-bold uppercase text-gray-400 block mb-1">
                  Critères d'évaluation associés :
                </span>
                <div className="flex flex-wrap gap-2 text-xs">
                  {Object.entries(rec.criteres_evalues).map(([key, val], i) => (
                    <span key={i} className="bg-gray-100 border border-gray-200 px-2.5 py-1 rounded-lg text-gray-600">
                      <b>{key}</b> : {String(val)}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* SECTION 3 : DECISION PATH & TRAÇABILITÉ */}
      <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm space-y-3">
        <div className="flex items-center justify-between border-b pb-3">
          <div className="flex items-center gap-2 text-[#1F3D4D]">
            <ShieldCheck className="w-5 h-5 text-[#1D7893]" />
            <h2 className="font-bold text-sm uppercase tracking-wide">Traçabilité du Chemin Décisionnel (Decision Path)</h2>
          </div>
          <span className="text-xs text-gray-400">{totalRegles} Règles Évaluées</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-emerald-50/60 rounded-xl border border-emerald-100">
            <span className="text-emerald-800 block">Règles Déclenchées</span>
            <span className="font-bold text-emerald-900 text-sm">{reglesDeclencheesCount}</span>
          </div>
          <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
            <span className="text-gray-500 block">Non Déclenchées</span>
            <span className="font-bold text-gray-600 text-sm">{reglesNonDeclencheesCount}</span>
          </div>
          <div className="p-3 bg-amber-50/50 rounded-xl border border-amber-100">
            <span className="text-amber-700 block">Ignorées (Champs manquants)</span>
            <span className="font-bold text-amber-800 text-sm">{reglesIgnoreesCount}</span>
          </div>
        </div>
      </div>

    </div>
  );
}