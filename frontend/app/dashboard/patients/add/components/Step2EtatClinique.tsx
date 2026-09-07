"use client";

import { ChangeEvent } from "react";

interface Step2Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step2EtatClinique({ data, updateData, onNext, onPrev }: Step2Props) {
  const calculatePatientNonOperable = (comorbidites: boolean, nutrition: string, ecogScore: number) => {
    return comorbidites || nutrition === "dénutrition sévère" || ecogScore >= 3;
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    let updatedValue: any = value;

    if (type === "checkbox") {
      updatedValue = (e.target as HTMLInputElement).checked;
    } else if (name === "ecog") {
      updatedValue = parseInt(value, 10);
    }

    const nextState = { ...data, [name]: updatedValue };
    const isNonOperable = calculatePatientNonOperable(
      nextState.comorbiditesLourdes,
      nextState.etatNutritionnel,
      nextState.ecog
    );

    updateData({
      [name]: updatedValue,
      patientNonOperable: isNonOperable,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="border-b border-gray-100 pb-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 2 : État Général et Clinique (A.2)</h2>
          <p className="text-xs text-gray-500 mt-0.5">Évaluation du score ECOG, nutrition et symptômes</p>
        </div>
        <div className={`px-3 py-1.5 rounded-xl text-[11px] font-bold border ${
          data.patientNonOperable
            ? "bg-amber-50 text-amber-700 border-amber-200"
            : "bg-emerald-50 text-emerald-700 border-emerald-200"
        }`}>
          Profil opératoire: {data.patientNonOperable ? "Non opérable (R3)" : "Opérable sous réserve"}
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">ECOG / Performance Status *</label>
          <select
            name="ecog"
            value={data.ecog}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value={0}>0 </option>
            <option value={1}>1 </option>
            <option value={2}>2 </option>
            <option value={3}>3 </option>
            <option value={4}>4 </option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">État nutritionnel *</label>
          <select
            name="etatNutritionnel"
            value={data.etatNutritionnel}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="normal">Normal</option>
            <option value="dénutrition modérée">Dénutrition modérée</option>
            <option value="dénutrition sévère">Dénutrition sévère (Non opérable)</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Diabète</label>
          <select
            name="diabete"
            value={data.diabete}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="absent">Absent</option>
            <option value="récent (<2 ans)">Récent (&lt; 2 ans)</option>
            <option value="ancien">Ancien</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Douleur</label>
          <div className="flex gap-2">
            <select
              name="douleur"
              value={data.douleur}
              onChange={handleChange}
              className="w-1/2 px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
            >
              <option value="absente">Absente</option>
              <option value="présente">Présente</option>
            </select>
            {data.douleur === "présente" && (
              <input
                type="text"
                name="intensiteDouleur"
                placeholder="Intensité / Détails..."
                value={data.intensiteDouleur}
                onChange={handleChange}
                className="w-1/2 px-3 py-2.5 rounded-xl border border-gray-200 text-xs"
              />
            )}
          </div>
        </div>

        <div className="sm:col-span-2 bg-gray-50 p-4 rounded-xl space-y-3 border border-gray-100">
          <span className="block font-bold text-[#1F3D4D] mb-1">Facteurs de risque et symptômes associés</span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="comorbiditesLourdes"
                checked={data.comorbiditesLourdes}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Comorbidités lourdes (Non opérable)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="ictere"
                checked={data.ictere}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Ictère (Urgence drainage T1 si associé)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="angiocholite"
                checked={data.angiocholite}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Angiocholite (T1)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="cholestase"
                checked={data.cholestase}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Cholestase (R2, T1)</span>
            </label>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onPrev}
          className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          ← Précédent : Démographie
        </button>
        <button
          type="submit"
          className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
        >
          <span>Suivant : Biologie (A.3)</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </div>
    </form>
  );
}