"use client";

import { useState } from "react";
import { 
  CheckCircle2, 
  AlertCircle, 
  FileText, 
  UserCheck, 
  ChevronRight, 
  Activity, 
  ShieldCheck,
  Building2,
  Stethoscope
} from "lucide-react";

export default function EvaluationPage() {
  // Simulation des données JSON reçues du moteur de règles
  const evaluationData = {
    id_decision: 3,
    id_evaluation: 19,
    date_decision: "2026-09-07T13:03:53.499Z",
    source_code: "TNCD-2024",
    source_version: "17/05/2024",
    facts: {
      age: 66,
      ecog: 1,
      ca19_9: 620,
      ictere: true,
      bilirubine: 45,
      cholestase: true,
      metastases: false,
      resecabilite: "resecable",
      stade_global: "IB",
      categorie_t: "T2",
      categorie_n: "N0",
      categorie_m: "M0",
      adenopathie_distance: false,
      statut_dpd: "normal"
    },
    // Règle R1 ciblée selon le référentiel TNCD
    rule_r1: {
      code: "R01",
      titre: "Chirurgie d'emblée puis traitement adjuvant (Profil idéal)",
      grade: "Grade A",
      reference: "TNCD 9.4.1.1 / 9.4.1.3",
      recommandation_principale: "Proposition : discuter en RCP une chirurgie à visée curative (DPC ou SPG selon la localisation) dans un centre expert.",
      recommandation_secondaire: "En l'absence de contre-indication, prévoir une chimiothérapie adjuvante de 6 mois, avec mFOLFIRINOX en 1ère intention si l'état général et les comorbidités le permettent.",
      criteres_evalues: [
        { label: "Résécabilité anatomique", valeur: "Résécable", attendu: "Résécable", valide: true },
        { label: "Métastases à distance", valeur: "Non", attendu: "Non", valide: true },
        { label: "Adénopathie à distance", valeur: "Non", attendu: "Non", valide: true },
        { label: "Marqueur CA 19-9", valeur: "620 U/mL", attendu: "≤ 500 U/mL ou non renseigné", valide: false },
        { label: "Performance Status (ECOG)", valeur: "1", attendu: "≤ 1", valide: true }
      ]
    },
    decision_path_summary: {
      regles_evaluees: 22,
      regles_ignorees_donnees_manquantes: 10,
      regles_non_declenchees: 12,
      necessite_rcp: false
    }
  };

  const { facts, rule_r1, decision_path_summary } = evaluationData;

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
              Réf : {evaluationData.source_code} ({evaluationData.source_version})
            </span>
          </div>
          <h1 className="text-xl font-bold text-[#1F3D4D] mt-1">
            Rapport d'Aide à la Décision Clinique
          </h1>
        </div>
        <div className="text-right text-xs text-gray-500">
          <p>Évaluation N° : <span className="font-semibold text-gray-700">#{evaluationData.id_evaluation}</span></p>
          <p>Date : <span className="font-semibold text-gray-700">{new Date(evaluationData.date_decision).toLocaleDateString("fr-FR")}</span></p>
        </div>
      </div>

      {/* SECTION 1 : RESUME CLINIQUE DU PATIENT */}
      <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-[#1F3D4D] border-b pb-3">
          <Activity className="w-5 h-5 text-[#1D7893]" />
          <h2 className="font-bold text-sm uppercase tracking-wide">Résumé Clinique du Patient</h2>
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
            <span className="text-gray-400 block mb-1">ECOG / Statut Général</span>
            <span className="font-bold text-[#1F3D4D] text-sm">ECOG {facts.ecog}</span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Biologie Clé</span>
            <span className="font-bold text-[#1F3D4D] text-sm">CA19-9 : {facts.ca19_9} U/mL</span>
          </div>
        </div>

        {/* Détails complémentaires */}
        <div className="flex flex-wrap gap-2 text-xs pt-1">
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Âge: <b>{facts.age} ans</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Métastases: <b>Non</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Adénopathie à distance: <b>Non</b></span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Ictère / Cholestase: <b>Oui</b> (Bilirubine: {facts.bilirubine} µmol/L)</span>
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Statut DPD: <b>{facts.statut_dpd}</b></span>
        </div>
      </div>

      {/* SECTION 2 : RECOMMANDATION RÈGLE R01 */}
      <div className="bg-white rounded-2xl border border-emerald-200 shadow-sm overflow-hidden">
        
        {/* En-tête Recommandation */}
        <div className="bg-emerald-50/70 p-5 border-b border-emerald-100 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500 text-white p-2 rounded-xl">
              <Stethoscope className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-emerald-900 text-sm">{rule_r1.code} — {rule_r1.titre}</span>
                <span className="bg-emerald-200/60 text-emerald-800 font-semibold text-[10px] px-2 py-0.5 rounded">
                  {rule_r1.grade}
                </span>
              </div>
              <p className="text-xs text-emerald-700 mt-0.5">Référence : {rule_r1.reference}</p>
            </div>
          </div>
        </div>

        {/* Corps des recommandations */}
        <div className="p-6 space-y-4">
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wide text-gray-400">Recommandation Principale</h3>
            <div className="p-4 bg-emerald-50/40 border-l-4 border-emerald-500 text-gray-800 text-sm font-medium rounded-r-xl">
              {rule_r1.recommandation_principale}
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wide text-gray-400">Prise en Charge Adjuvante</h3>
            <div className="p-4 bg-gray-50 border-l-4 border-gray-300 text-gray-700 text-xs rounded-r-xl">
              {rule_r1.recommandation_secondaire}
            </div>
          </div>

          {/* Analyse de conformité des critères */}
          <div className="pt-2">
            <h3 className="text-xs font-bold uppercase tracking-wide text-gray-400 mb-3">
              Analyse des Critères d'Ajustement (Règle R01)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              {rule_r1.criteres_evalues.map((critere, idx) => (
                <div 
                  key={idx} 
                  className={`p-3 rounded-xl border flex justify-between items-center ${
                    critere.valide ? "bg-white border-gray-100" : "bg-amber-50/50 border-amber-200"
                  }`}
                >
                  <div>
                    <span className="text-gray-500 block">{critere.label}</span>
                    <span className="font-semibold text-gray-800">Saisi: {critere.valeur}</span>
                  </div>
                  <div className="text-right">
                    {critere.valide ? (
                      <span className="inline-flex items-center gap-1 text-emerald-600 font-semibold">
                        <CheckCircle2 className="w-4 h-4" /> Conforme
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-amber-600 font-semibold" title={`Attendu: ${critere.attendu}`}>
                        <AlertCircle className="w-4 h-4" /> Élevé (R02)
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* SECTION 3 : RESUME DU CHEMIN DECISIONNEL */}
      <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm space-y-3">
        <div className="flex items-center justify-between border-b pb-3">
          <div className="flex items-center gap-2 text-[#1F3D4D]">
            <ShieldCheck className="w-5 h-5 text-[#1D7893]" />
            <h2 className="font-bold text-sm uppercase tracking-wide">Résumé du Chemin Décisionnel</h2>
          </div>
          <span className="text-xs text-gray-400">22 Règles Analysées au Total</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
            <span className="text-gray-500 block">Règles Évaluées</span>
            <span className="font-bold text-gray-800 text-sm">{decision_path_summary.regles_evaluees}</span>
          </div>
          <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
            <span className="text-gray-500 block">Non Déclenchées</span>
            <span className="font-bold text-gray-600 text-sm">{decision_path_summary.regles_non_declenchees}</span>
          </div>
          <div className="p-3 bg-amber-50/50 rounded-xl border border-amber-100">
            <span className="text-amber-700 block">Ignorées (Données manquantes)</span>
            <span className="font-bold text-amber-800 text-sm">{decision_path_summary.regles_ignorees_donnees_manquantes}</span>
          </div>
        </div>

        <p className="text-[11px] text-gray-400 pt-2 italic">
          * Note : Le CA19-9 étant &gt; 500 U/mL (620 U/mL), l'équipe médicale peut également évaluer la règle <b>R02</b> (discussion de chimio-néoadjuvante en RCP).
        </p>
      </div>

    </div>
  );
}