"use client";

import { ChangeEvent } from "react";

interface Step5Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step5Tnm({ data, updateData, onNext, onPrev }: Step5Props) {
  const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    updateData({ [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="border-b border-gray-100 pb-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 5 : Classification TNM</h2>
          <p className="text-xs text-gray-500 mt-0.5">Staging anatomique de la maladie </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 text-xs">
        
        {/* Catégorie T */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Catégorie T *</label>
          <select
            name="categorieT"
            value={data.categorieT || "T1a"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="T1a">T1a (Tumeur ≤ 0,5 cm)</option>
            <option value="T1b">T1b (Tumeur &gt; 0,5 cm et &lt; 1 cm)</option>
            <option value="T1c">T1c (Tumeur 1 à 2 cm)</option>
            <option value="T2">T2 (Tumeur &gt; 2 cm et ≤ 4 cm)</option>
            <option value="T3">T3 (Tumeur &gt; 4 cm)</option>
            <option value="T4">T4 (Atteinte du TC, de l'AMS et/ou de l'AHC)</option>
          </select>
        </div>

        {/* Catégorie N */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Catégorie N *</label>
          <select
            name="categorieN"
            value={data.categorieN || "N0"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="N0">N0 (Pas de métastase ganglionnaire régionale)</option>
            <option value="N1">N1 (1 à 3 adénopathies régionales)</option>
            <option value="N2">N2 (≥ 4 adénopathies régionales)</option>
          </select>
        </div>

        {/* Catégorie M */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Catégorie M *</label>
          <select
            name="categorieM"
            value={data.categorieM || "M0"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="M0">M0 (Pas de métastase à distance)</option>
            <option value="M1">M1 (Présence de métastase(s) à distance)</option>
          </select>
        </div>

      </div>

      {/* BOUTONS NAVIGATION */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onPrev}
          className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          ← Précédent : Imagerie
        </button>
        <button
          type="submit"
          className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
        >
          <span>Suivant : Histologie (A.6)</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </div>
    </form>
  );
}