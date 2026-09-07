"use client";

import { ChangeEvent } from "react";

interface Step3Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step3Biologie({ data, updateData, onNext, onPrev }: Step3Props) {
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    updateData({
      [name]: value === "" ? "" : isNaN(Number(value)) ? value : Number(value),
    });
  };

  const ratioBilirubine =
    data.bilirubine !== "" && data.lsnBilirubine !== "" && Number(data.lsnBilirubine) > 0
      ? (Number(data.bilirubine) / Number(data.lsnBilirubine)).toFixed(2)
      : null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="border-b border-gray-100 pb-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 3 : Bilan Biologique </h2>
          <p className="text-xs text-gray-500 mt-0.5">Saisie des biomarqueurs et paramètres biologiques</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
        {/* CA 19-9 */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">CA 19-9 (U/mL)</label>
          <input
            type="number"
            name="ca199"
            placeholder="ex. 620"
            value={data.ca199}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
          <span className="text-[10px] text-gray-400 mt-1 block">Seuil critique : 500 U/mL </span>
        </div>

        {/* Statut DPD */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Statut DPD *</label>
          <select
            name="statutDpd"
            value={data.statutDpd}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="normal">Normal</option>
            <option value="déficit partiel">Déficit partiel</option>
            <option value="déficit complet">Déficit complet</option>
          </select>
        </div>

        {/* Bilirubine */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Bilirubine totale (µmol/L)</label>
          <input
            type="number"
            name="bilirubine"
            placeholder="ex. 45"
            value={data.bilirubine}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
          <span className="text-[10px] text-gray-400 mt-1 block">Seuil T1 : 250 µmol/L</span>
        </div>

        {/* LSN Bilirubine */}
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">LSN Bilirubine  (µmol/L)</label>
          <input
            type="number"
            name="lsnBilirubine"
            placeholder="ex. 21"
            value={data.lsnBilirubine}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
          {ratioBilirubine !== null && (
            <span className="text-[10px] font-semibold text-[#1D7893] mt-1 block">
              Calcul : {ratioBilirubine} × LSN
            </span>
          )}
        </div>

        {/* Albuminémie */}
        <div className="sm:col-span-2">
          <label className="block text-gray-700 font-semibold mb-1.5">Albuminémie (g/L)</label>
          <input
            type="number"
            name="albuminemie"
            placeholder="ex. 32"
            value={data.albuminemie}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onPrev}
          className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          ← Précédent
        </button>
        <button
          type="submit"
          className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
        >
          <span>Suivant : Imagerie (A.4)</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </div>
    </form>
  );
}