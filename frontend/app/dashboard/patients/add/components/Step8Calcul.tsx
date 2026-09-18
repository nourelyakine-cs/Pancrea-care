"use client";
import { Activity, ArrowLeft, ArrowRight, Loader2 } from "lucide-react";
import type { ClinicalResult } from "../../../../../lib/api";

interface Step8CalculProps { result?: ClinicalResult | null; loading?: boolean; error?: string | null; onPrev: () => void; onNext: () => void; }
const label = (value: string | null | undefined) => value || "Non calculé";

export default function Step8Calcul({ result = null, loading = false, error = null, onPrev, onNext }: Step8CalculProps) {
  return <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-6">
    <div className="flex items-center gap-3 border-b pb-4"><div className="bg-[#1D7893]/10 p-3 rounded-xl text-[#1D7893]"><Activity className="w-6 h-6" /></div><div><h2 className="text-lg font-bold text-[#1F3D4D]">Étape de Calcul & Aide à la Décision</h2><p className="text-xs text-gray-500">Résultats calculés par le moteur backend TNCD.</p></div></div>
    {loading && <div className="flex items-center gap-2 rounded-xl bg-cyan-50 p-4 text-sm text-[#1D7893]"><Loader2 className="h-4 w-4 animate-spin" /> Création du dossier et calcul des résultats…</div>}
    {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><b>Calcul impossible :</b> {error}</div>}
    {result && !loading && <div className="grid grid-cols-1 md:grid-cols-3 gap-4"><ResultCard title="Critères ABC" value={label(result.sous_categorie_abc)} detail={`B : ${result.critere_abc_b ? "positif" : "négatif"} · C : ${result.critere_abc_c ? "positif" : "négatif"}`} /><ResultCard title="Stade TNM" value={label(result.stade_global)} detail={`${label(result.categorie_t)} ${label(result.categorie_n)} ${label(result.categorie_m)}`} /><ResultCard title="Résécabilité" value={label(result.resecabilite)} detail={result.resecabilite === "resecable" ? "Anatomiquement résécable" : "Patient à discuter en RCP"} /></div>}
    <div className="flex justify-between pt-4 border-t"><button type="button" onClick={onPrev} className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50"><ArrowLeft className="w-4 h-4" /> Retour aux formulaires</button><button type="button" onClick={onNext} disabled={!result || loading} className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-[#1D7893] hover:bg-[#209BBF] disabled:opacity-50 text-white text-xs font-semibold shadow-md transition-all">Voir le Rapport d&apos;Évaluation <ArrowRight className="w-4 h-4" /></button></div>
  </div>;
}
function ResultCard({ title, value, detail }: { title: string; value: string; detail: string }) { return <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2"><span className="text-xs text-gray-400 font-semibold uppercase tracking-wider">{title}</span><div className="flex justify-between items-center"><span className="text-sm font-bold text-[#1F3D4D]">Résultat :</span><span className="bg-[#1D7893] text-white px-3 py-1 rounded-full text-xs font-extrabold">{value}</span></div><p className="text-[11px] text-gray-600 pt-2 border-t border-gray-200">{detail}</p></div>; }
