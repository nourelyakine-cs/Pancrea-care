"use client";

import { ChangeEvent } from "react";

interface Step1Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onNext: () => void;
}

export default function Step1Demographie({ data, updateData, onNext }: Step1Props) {
  const handleDateChange = (e: ChangeEvent<HTMLInputElement>) => {
    const dateStr = e.target.value;
    let calculatedAge: number | "" = "";

    if (dateStr) {
      const birthDate = new Date(dateStr);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();

      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      calculatedAge = age > 0 ? age : 0;
    }

    updateData({
      dateNaissance: dateStr,
      age: calculatedAge,
    });
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    updateData({ [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!data.nom || !data.prenom || !data.dateNaissance || !data.sexe) {
      alert("Veuillez remplir au moins le Nom, Prénom, Sexe et la Date de naissance.");
      return;
    }
    onNext();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
      <div className="border-b border-gray-100 pb-4">
        <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 1 : Données Démographiques (A.1)</h2>
        <p className="text-xs text-gray-500 mt-0.5">Informations d'identification générales du patient</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Nom *</label>
          <input
            type="text"
            name="nom"
            required
            value={data.nom}
            onChange={handleChange}
            placeholder="ex. Benali"
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Prénom *</label>
          <input
            type="text"
            name="prenom"
            required
            value={data.prenom}
            onChange={handleChange}
            placeholder="ex. Mohamed"
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Sexe *</label>
          <select
            name="sexe"
            required
            value={data.sexe}
            onChange={handleChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
          >
            <option value="">Sélectionner...</option>
            <option value="M">Masculin (M)</option>
            <option value="F">Féminin (F)</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Date de Naissance *</label>
          <input
            type="date"
            name="dateNaissance"
            required
            value={data.dateNaissance}
            onChange={handleDateChange}
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Numéro de téléphone</label>
          <input
            type="tel"
            name="telephone"
            value={data.telephone}
            onChange={handleChange}
            placeholder="ex. 0550 12 34 56"
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>

        <div>
          <label className="block text-gray-700 font-semibold mb-1.5">Adresse</label>
          <input
            type="text"
            name="adresse"
            value={data.adresse}
            onChange={handleChange}
            placeholder="ex. Alger, Bab El Oued"
            className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
          />
        </div>
      </div>

      <div className="flex justify-end pt-4 border-t border-gray-100">
        <button
          type="submit"
          className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
        >
          <span>Suivant : État Clinique (A.2)</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </div>
    </form>
  );
}