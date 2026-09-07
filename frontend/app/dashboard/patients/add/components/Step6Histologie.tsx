"use client";

import { ChangeEvent } from "react";

interface Step6Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step6Histologie({ data, updateData, onNext, onPrev }: Step6Props) {
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    let updatedValue: any = value;
    if (type === "checkbox") {
      updatedValue = (e.target as HTMLInputElement).checked;
    }

    updateData({ [name]: updatedValue });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="border-b border-gray-100 pb-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 6 : Histologie et Biologie Moléculaire </h2>
          <p className="text-xs text-gray-500 mt-0.5">Preuve histologique et profilage génomique / biomarqueurs</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
        
        {/* Preuve histologique */}
        <div className="sm:col-span-2 bg-gray-50 p-4 rounded-xl border border-gray-100">
          <label className="flex items-center gap-2 cursor-pointer font-bold text-[#1F3D4D]">
            <input
              type="checkbox"
              name="preuveHistologique"
              checked={!!data.preuveHistologique}
              onChange={handleChange}
              className="w-4 h-4 rounded text-[#1D7893]"
            />
            <span>Preuve histologique obtenue (Garde-fou T4)</span>
          </label>
          <span className="text-[10px] text-gray-400 mt-1 block pl-6">
            Obligatoire pour la confirmation diagnostique avant traitement médical.
          </span>
        </div>

        {/* Statut BRCA */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Statut BRCA *</label>
          <select
            name="statutBrca"
            value={data.statutBrca || "non testé"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="non testé">Non testé</option>
            <option value="muté">Muté </option>
            <option value="non muté">Non muté</option>
          </select>
        </div>

        {/* Statut KRAS */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Statut KRAS *</label>
          <select
            name="statutKras"
            value={data.statutKras || "non testé"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="non testé">Non testé</option>
            <option value="sauvage">Sauvage (Wild-type)</option>
            <option value="G12C">G12C </option>
            <option value="G12D">G12D</option>
            <option value="G12V">G12V</option>
            <option value="autre">Autre mutation</option>
          </select>
        </div>

        {/* Statut MSI / dMMR */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Statut MSI / dMMR *</label>
          <select
            name="statutMsiDmmr"
            value={data.statutMsiDmmr || "non testé"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="non testé">Non testé</option>
            <option value="positif">Positif (Instabilité microsatellitaire )</option>
            <option value="négatif">Négatif (Stable)</option>
          </select>
        </div>

        {/* Fusion NTRK */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Fusion NTRK *</label>
          <select
            name="fusionNtrk"
            value={data.fusionNtrk || "non testé"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="non testé">Non testé</option>
            <option value="oui">Oui (Présente )</option>
            <option value="non">Non</option>
          </select>
        </div>

        {/* Fusion NRG1 */}
        <div className="sm:col-span-2">
          <label className="block text-gray-700 font-semibold mb-1.5">Fusion NRG1 *</label>
          <select
            name="fusionNrg1"
            value={data.fusionNrg1 || "non testé"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="non testé">Non testé</option>
            <option value="oui">Oui (Présente)</option>
            <option value="non">Non</option>
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
          ← Précédent : TNM
        </button>
        <button
          type="submit"
          className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
        >
          <span>Suivant : Parcours Thérapeutique (A.7)</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </div>
    </form>
  );
}