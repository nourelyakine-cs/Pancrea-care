"use client";

import { Activity, ArrowLeft, ArrowRight } from "lucide-react";

interface Step8CalculProps {
  onPrev: () => void;
  onNext: () => void;
}

export default function Step8Calcul({ onPrev, onNext }: Step8CalculProps) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="flex items-center gap-3 border-b pb-4">
        <div className="bg-[#1D7893]/10 p-3 rounded-xl text-[#1D7893]">
          <Activity className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape de Calcul & Aide à la Décision</h2>
          <p className="text-xs text-gray-500">Résultats générés automatiquement par le système CDSS sur la base des données saisies.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* CALCUL ABC STATIQUE */}
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
          <span className="text-xs text-gray-400 font-semibold uppercase tracking-wider">Critères ABC</span>
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-[#1F3D4D]">Type ABC :</span>
            <span className="bg-[#1D7893] text-white px-3 py-1 rounded-full text-xs font-extrabold">AB</span>
          </div>
          <ul className="text-[11px] text-gray-600 space-y-1 pt-2 border-t border-gray-200">
            <li>• Critère B : <b className="text-emerald-600">Positif</b> (CA19-9 &gt; 500)</li>
            <li>• Critère C : <b className="text-gray-500">Négatif</b> (ECOG &lt; 2)</li>
          </ul>
        </div>

        {/* CALCUL STADE TNM STATIQUE */}
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
          <span className="text-xs text-gray-400 font-semibold uppercase tracking-wider">Stade TNM</span>
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-[#1F3D4D]">Stade Global :</span>
            <span className="bg-emerald-600 text-white px-3 py-1 rounded-full text-xs font-extrabold">Stade IB</span>
          </div>
          <p className="text-[11px] text-gray-600 pt-2 border-t border-gray-200">
            Formule appliquée : <b>T2 N0 M0</b> (Absence de métastases à distance).
          </p>
        </div>

        {/* CALCUL RESECABILITE STATIQUE */}
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
          <span className="text-xs text-gray-400 font-semibold uppercase tracking-wider">Résécabilité & Opérabilité</span>
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-[#1F3D4D]">Statut :</span>
            <span className="bg-emerald-100 text-emerald-800 border border-emerald-300 px-3 py-1 rounded-full text-xs font-bold capitalize">Résécable</span>
          </div>
          <p className="text-[11px] text-gray-600 pt-2 border-t border-gray-200">
            Opérabilité : <b className="text-emerald-600">Patient Opérable</b>
          </p>
        </div>
      </div>

      <div className="flex justify-between pt-4 border-t">
        <button
          type="button"
          onClick={onPrev}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 text-xs font-semibold hover:bg-gray-50"
        >
          <ArrowLeft className="w-4 h-4" /> Retour aux formulaires
        </button>
        <button
          type="button"
          onClick={onNext}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold shadow-md transition-all"
        >
          Voir le Rapport d'Évaluation <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}