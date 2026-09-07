"use client";

import { ChangeEvent } from "react";

interface Step4Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step4Imagerie({ data, updateData, onNext, onPrev }: Step4Props) {
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    let updatedValue: any = value;
    if (type === "checkbox") {
      updatedValue = (e.target as HTMLInputElement).checked;
    } else if (type === "number") {
      updatedValue = value === "" ? "" : Number(value);
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
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 4 : Imagerie et Anatomie Tumoration (A.4)</h2>
          <p className="text-xs text-gray-500 mt-0.5">Évaluation des contacts vasculaires et de l'extension tumorale</p>
        </div>
        {data.metastases && (
          <span className="px-3 py-1.5 rounded-xl text-[11px] font-bold bg-red-50 text-red-700 border border-red-200">
            Branche Métastatique
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
        
        {/* Localisation tumorale */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Localisation tumorale *</label>
          <select
            name="localisationTumorale"
            value={data.localisationTumorale || "tête/crochet"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="tête/crochet">Tête / Crochet</option>
            <option value="corps-queue">Corps / Queue</option>
          </select>
        </div>

        {/* Taille tumorale */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Taille tumorale (cm)</label>
          <input
            type="number"
            step="0.1"
            name="tailleTumorale"
            placeholder="ex. 3.2"
            value={data.tailleTumorale ?? ""}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
          <span className="text-[10px] text-gray-400 mt-1 block">Utilisé uniquement pour le TNM</span>
        </div>

        {/* Contact AMS */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Contact Arteria Mesenterica Superior (AMS) *</label>
          <select
            name="contactAms"
            value={data.contactAms || "pas de contact"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="pas de contact">Pas de contact</option>
            <option value="<180°">&lt; 180°</option>
            <option value="≥180°">≥ 180°</option>
          </select>
        </div>

        {/* Contact Tronc Cœliaque */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Contact Tronc Cœliaque *</label>
          <select
            name="contactTroncCoeliaque"
            value={data.contactTroncCoeliaque || "pas de contact"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="pas de contact">Pas de contact</option>
            <option value="<180°">&lt; 180°</option>
            <option value="≥180°">≥ 180°</option>
          </select>
        </div>

        {/* Contact AHC */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Contact Artère Hépatique Commune (AHC) *</label>
          <select
            name="contactAhc"
            value={data.contactAhc || "pas de contact"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="pas de contact">Pas de contact</option>
            <option value="court reconstructible">Court reconstructible</option>
            <option value="non reconstructible">Non reconstructible</option>
          </select>
        </div>

        {/* Contact VMS / VP */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Contact VMS / Veine Porte *</label>
          <select
            name="contactVmsVp"
            value={data.contactVmsVp || "<180° sans irrégularité"}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="<180° sans irrégularité">&lt; 180° sans irrégularité</option>
            <option value="≥180° ou irrégularité ou occlusion reconstructible">≥ 180° / irrégularité / occlusion reconstructible</option>
            <option value="occlusion non reconstructible">Occlusion non reconstructible</option>
          </select>
        </div>

        {/* CASES À COCHER : Extension ganglionnaire et Métastases */}
        <div className="sm:col-span-2 bg-gray-50 p-4 rounded-xl space-y-3 border border-gray-100">
          <span className="block font-bold text-[#1F3D4D] mb-1">Adénopathies et Métastases</span>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="adenopathieRegionale"
                checked={!!data.adenopathieRegionale}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Adénopathie régionale</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="adenopathieDistance"
                checked={!!data.adenopathieDistance}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span>Adénopathie à distance (T2)</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                name="metastases"
                checked={!!data.metastases}
                onChange={handleChange}
                className="w-4 h-4 rounded text-[#1D7893]"
              />
              <span className="font-semibold text-red-600">Métastases à distance</span>
            </label>

          </div>
        </div>

      </div>

      {/* BOUTONS NAVIGATION */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onPrev}
          className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          ← Précédent : Biologie
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