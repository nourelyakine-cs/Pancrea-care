"use client";

import { useEffect, useState, use } from "react";
import { 
  Activity, 
  ShieldCheck,
  Stethoscope,
  AlertTriangle,
  Loader2
} from "lucide-react";
import { getRecommendations, type RecommendationsResponse } from "@/lib/api";

interface EvaluationPageProps {
  params?: Promise<{ id?: string }>;
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
  patientId?: string;
  idEvaluation?: number | null;
  recommendationsData?: RecommendationsResponse | null;
  data?: any;
}

function scalar(value: string | string[] | undefined): string | null {
  if (Array.isArray(value)) return value[0] ?? null;
  return value ?? null;
}

export default function EvaluationPage({
  params,
  searchParams,
  patientId: propPatientId,
  idEvaluation,
  recommendationsData: initialData,
  data
}: EvaluationPageProps) {
  const resolvedParams = params ? use(params) : null;
  const resolvedSearch = searchParams ? use(searchParams) : null;

  const queryEvalId = scalar(resolvedSearch?.evalId);
  const effectiveEvalId = idEvaluation ?? (queryEvalId ? Number(queryEvalId) || null : null) ?? null;
  const currentPatientId =
    propPatientId ||
    resolvedParams?.id ||
    scalar(resolvedSearch?.patientId) ||
    "PAT-CURRENT";

  const [evaluationData, setEvaluationData] = useState<RecommendationsResponse | null>(initialData || null);
  const [loading, setLoading] = useState<boolean>(!initialData && Boolean(effectiveEvalId));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialData) {
      setEvaluationData(initialData);
      return;
    }
    if (effectiveEvalId) {
      setLoading(true);
      getRecommendations(effectiveEvalId)
        .then((res) => setEvaluationData(res))
        .catch((err) => setError(err.message || "Impossible de charger les recommandations"))
        .finally(() => setLoading(false));
    }
  }, [effectiveEvalId, initialData]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-white rounded-2xl border border-gray-100 shadow-sm space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#1D7893]" />
        <p className="text-sm font-medium text-gray-600">Chargement du rapport d'évaluation CDSS...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
        <b>Erreur de chargement des recommandations :</b> {error}
      </div>
    );
  }

  if (!evaluationData) {
    return (
      <div className="p-6 bg-gray-50 border border-gray-200 rounded-2xl text-gray-500 text-center text-sm">
        Aucune donnée d'évaluation disponible. Veuillez valider l'étape précédente pour calculer le rapport.
      </div>
    );
  }

  const { 
    facts = {}, 
    recommendations = [], 
    decision_path = [], 
    regles_declenchees = [],
    necessite_rcp = false,
    source_code = "TNCD",
    source_version = "2024",
    id_evaluation = effectiveEvalId
  } = evaluationData;

  const totalRegles = decision_path.length;
  const reglesDeclencheesCount = decision_path.filter(r => r.statut === "declenchee" || regles_declenchees.includes(r.code)).length;
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
              Réf : {source_code} ({source_version}) — Patient : {currentPatientId}
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
            <p>Évaluation N° : <span className="font-semibold text-gray-700">#{id_evaluation || "N/A"}</span></p>
            <p>Date : <span className="font-semibold text-gray-700">{evaluationData.date_decision ? new Date(evaluationData.date_decision).toLocaleDateString("fr-FR") : new Date().toLocaleDateString("fr-FR")}</span></p>
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
            <span className="font-bold text-[#1F3D4D] text-sm">
              {facts.categorie_t || data?.categorieT || ""}{facts.categorie_n || data?.categorieN || ""}{facts.categorie_m || data?.categorieM || ""} 
              {facts.stade_global ? ` — Stade ${facts.stade_global}` : ""}
            </span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Résécabilité</span>
            <span className="font-bold text-emerald-600 text-sm capitalize">{facts.resecabilite || "Non déterminée"}</span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Critères ABC</span>
            <span className="font-bold text-amber-700 text-sm">
              Type {facts.type_abc || (facts.critere_abc_b ? "B" : "N/A")}
            </span>
          </div>
          <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
            <span className="text-gray-400 block mb-1">Biologie Clé</span>
            <span className="font-bold text-[#1F3D4D] text-sm">CA19-9 : {facts.ca19_9 ?? data?.ca199 ?? "N/A"} U/mL</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 text-xs pt-1">
          {facts.age && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Âge: <b>{facts.age} ans</b></span>}
          {facts.ecog !== undefined && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">ECOG: <b>{facts.ecog}</b></span>}
          {facts.metastases !== undefined && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Métastases: <b>{facts.metastases ? "Oui" : "Non"}</b></span>}
          {facts.ictere !== undefined && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Ictère / Cholestase: <b>{facts.ictere ? "Oui" : "Non"}</b> {facts.bilirubine ? `(Bilirubine: ${facts.bilirubine} µmol/L)` : ""}</span>}
          {facts.statut_dpd && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">Statut DPD: <b>{facts.statut_dpd}</b></span>}
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
                  <h3 className="font-bold text-emerald-900 text-sm">{rec.titre || `Recommandation ${rec.code}`}</h3>
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
              {rec.criteres_evalues && Object.keys(rec.criteres_evalues).length > 0 && (
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
              )}
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