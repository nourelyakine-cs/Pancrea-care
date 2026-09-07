"use client";

import { ChangeEvent, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";

interface Step7Props {
  data: any;
  updateData: (fields: Partial<any>) => void;
  onSubmitFinal: () => void;
  onPrev: () => void;
}

export default function Step7Parcours({ data, updateData, onSubmitFinal, onPrev }: Step7Props) {
  const router = useRouter();
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    let updatedValue: any = value;
    if (type === "checkbox") {
      updatedValue = (e.target as HTMLInputElement).checked;
    } else if (type === "number") {
      updatedValue = value === "" ? "" : Number(value);
    }

    updateData({ [name]: updatedValue });
  };

  const handleTraitementsRecusChange = (e: ChangeEvent<HTMLInputElement>) => {
    const textValue = e.target.value;
    const arrayValues = textValue.split(",").map((s) => s.trim()).filter(Boolean);
    const lastElement = arrayValues.length > 0 ? arrayValues[arrayValues.length - 1] : "";

    updateData({
      traitementsRecusTexte: textValue,
      traitementsRecus: arrayValues,
      lignePrecedente: lastElement,
    });
  };

  const handleOpenConfirm = (e: React.FormEvent) => {
    e.preventDefault();
    setShowConfirmModal(true);
  };

  const handleConfirmSave = () => {
    setShowConfirmModal(false);
    setIsSaved(true);

    // Appelle la fonction de soumission de données sans popup navigateur
    onSubmitFinal();

    // Redirection automatique vers le dashboard après 3 secondes (3000ms)
    setTimeout(() => {
      router.push("/dashboard/patients");
    }, 500);
  };

  return (
    <>
      <form onSubmit={handleOpenConfirm} className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-100 shadow-sm space-y-6">
        <div className="border-b border-gray-100 pb-4 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-bold text-[#1F3D4D]">Étape 7 : Parcours Thérapeutique</h2>
            <p className="text-xs text-gray-500 mt-0.5">Historique des lignes de traitement et suivi de l'évolution</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
          {/* Ligne de traitement actuelle */}
          <div>
            <label className="block text-gray-700 font-semibold mb-1.5">Ligne de traitement actuelle *</label>
            <select
              name="ligneTraitementActuelle"
              value={data.ligneTraitementActuelle || 1}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
            >
              <option value={1}>1ère ligne</option>
              <option value={2}>2ème ligne</option>
              <option value={3}>3ème ligne</option>
            </select>
          </div>

          {/* Réponse au traitement en cours */}
          <div>
            <label className="block text-gray-700 font-semibold mb-1.5">Réponse au traitement en cours *</label>
            <select
              name="reponseTraitementEnCours"
              value={data.reponseTraitementEnCours || "stable"}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs bg-white focus:outline-none focus:border-[#209BBF]"
            >
              <option value="réponse">Réponse</option>
              <option value="stable">Stable</option>
              <option value="progression">Progression</option>
            </select>
          </div>

          {/* Traitements déjà reçus */}
          <div className="sm:col-span-2">
            <label className="block text-gray-700 font-semibold mb-1.5">Traitements déjà reçus (séparés par des virgules)</label>
            <input
              type="text"
              name="traitementsRecusTexte"
              placeholder="ex. FOLFIRINOX, Gemcitabine"
              value={data.traitementsRecusTexte ?? ""}
              onChange={handleTraitementsRecusChange}
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
            />
            {data.lignePrecedente && (
              <span className="text-[10px] font-semibold text-[#1D7893] mt-1 block">
                Dernier traitement calculé : {data.lignePrecedente}
              </span>
            )}
          </div>

          {/* Durée chimiothérapie */}
          <div>
            <label className="block text-gray-700 font-semibold mb-1.5">Durée chimiothérapie (mois)</label>
            <input
              type="number"
              step="0.5"
              name="dureeChimiotherapieMois"
              placeholder="ex. 5"
              value={data.dureeChimiotherapieMois ?? ""}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
            />
            <span className="text-[10px] text-gray-400 mt-1 block">Seuil critique : ≥ 4 mois (R9)</span>
          </div>

          {/* Toxicité */}
          <div>
            <label className="block text-gray-700 font-semibold mb-1.5">Toxicité résiduelle (Détails)</label>
            <input
              type="text"
              name="detailsToxicite"
              placeholder="ex. Neuropathie grade 2"
              value={data.detailsToxicite ?? ""}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs focus:outline-none focus:border-[#209BBF]"
            />
          </div>

          {/* ÉVALUATIONS BOOLEENNES */}
          <div className="sm:col-span-2 bg-gray-50 p-4 rounded-xl space-y-3 border border-gray-100">
            <span className="block font-bold text-[#1F3D4D] mb-1">Évaluation clinique et planification</span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="tumeurControle"
                  checked={!!data.tumeurControle}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span>Tumeur contrôlée</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="nouvellesMetastases"
                  checked={!!data.nouvellesMetastases}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span className="text-red-600 font-semibold">Nouvelles métastases</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="pasDeProgressionApres16SemainesPlatine"
                  checked={!!data.pasDeProgressionApres16SemainesPlatine}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span>Pas de progression après 16 sem. de platine</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="toxiciteResiduelle"
                  checked={!!data.toxiciteResiduelle}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span>Toxicité résiduelle présente</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="chirurgieDembleePrevue"
                  checked={!!data.chirurgieDembleePrevue}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span>Chirurgie d'emblée prévue</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="traitementMedicalPrevu"
                  checked={!!data.traitementMedicalPrevu}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-[#1D7893]"
                />
                <span>Traitement médical prévu</span>
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
            ← Précédent : Histologie
          </button>
          <button
            type="submit"
            className="px-6 py-2.5 bg-[#1D7893] hover:bg-[#155b70] text-white text-xs font-semibold rounded-xl shadow-md transition flex items-center gap-2"
          >
            <span>✓ Finaliser & Enregistrer le Patient</span>
          </button>
        </div>
      </form>

      {/* MODALE VALIDATION : OUI / NON */}
      <AnimatePresence>
        {showConfirmModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white rounded-3xl max-w-sm w-full p-6 text-center shadow-2xl border border-gray-100 space-y-4"
            >
              <h3 className="text-base font-bold text-[#1F3D4D]">
                Voulez-vous valider ?
              </h3>
              <p className="text-xs text-gray-500">
                Confirmez-vous l'enregistrement de ce nouveau patient ?
              </p>

              <div className="flex items-center justify-center gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition w-1/2"
                >
                  Non
                </button>
                <button
                  type="button"
                  onClick={handleConfirmSave}
                  className="px-5 py-2.5 bg-[#1D7893] hover:bg-[#155b70] text-white text-xs font-semibold rounded-xl shadow-md transition w-1/2"
                >
                  Oui
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* CARTE DE SUCCÈS (AFFICHER PENDANT 3 SECONDES AVANT REDIRECTION) */}
      <AnimatePresence>
        {isSaved && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="bg-white rounded-3xl p-8 text-center space-y-4 shadow-2xl max-w-sm w-full border border-gray-100"
            >
              <div className="w-14 h-14 bg-[#1D7893]/10 text-[#1D7893] rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
                ✓
              </div>
              <h3 className="text-lg font-bold text-[#1F3D4D]">Patient enregistré avec succès !</h3>
              <p className="text-xs text-gray-400">Redirection vers le tableau de bord...</p>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}