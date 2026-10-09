"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import logoImg from "@/assets/logo.png";
import { forgotPassword } from "@/lib/api";

/**
 * Demande de réinitialisation de mot de passe.
 *
 * La plateforme n'a pas de service d'email : cette page n'envoie aucun lien.
 * Elle enregistre une demande que le super admin voit dans son tableau de bord
 * et à laquelle il répond par un lien à usage unique, transmis par téléphone ou
 * messagerie. Le libellé l'explique, sinon un médecin sans email reçu
 * conclurait que sa demande a échoué.
 *
 * Une demande de réinitialisation n'est pas une action anodine : elle bloque
 * l'accès au dossier d'un patient en cours de consultation. La page est donc
 * traitée comme un parcours d'urgence — signal ambré, héros mis en avant,
 * étapes numérotées — sans jamais promettre un délai de traitement que le
 * système ne peut pas garantir : la remise du lien est manuelle, et un
 * engagement de délai serait invérifiable.
 */
export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      const res = await forgotPassword(email);
      setMessage(res.message);
      setIsSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setIsLoading(false);
    }
  };

  const etapes = [
    "Vous saisissez votre adresse email professionnelle.",
    "La demande apparaît dans le tableau de bord de l'administration.",
    "Un administrateur vous transmet un lien, par téléphone ou messagerie.",
  ];

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-[#EAF4F7] via-[#F4FAFC] to-[#FFF7ED] flex items-center justify-center p-4 sm:p-6 font-serif relative overflow-hidden">
      {/* HALOS DÉCORATIFS : donnent de la profondeur au fond, qui était plat */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -top-24 -right-24 w-96 h-96 rounded-full bg-[#209BBF]/10 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -bottom-32 -left-24 w-[28rem] h-[28rem] rounded-full bg-amber-400/10 blur-3xl"
      />

      {/* BOUTON RETOUR CONNEXION */}
      <Link href="/login" className="absolute top-6 left-6 z-50">
        <motion.div
          whileHover={{ x: -4 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 text-sm font-semibold text-[#1D7893] hover:text-[#209BBF] transition-colors cursor-pointer"
        >
          <svg className="w-5 h-5 stroke-current" fill="none" viewBox="0 0 24 24" strokeWidth="2.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          <span>Retour à la connexion</span>
        </motion.div>
      </Link>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50"
      >
        {/* LOGO */}
        <div className="flex justify-center mb-5">
          <Image src={logoImg} alt="PANCRA CARE" width={150} height={45} className="h-10 w-auto object-contain" />
        </div>

        <AnimatePresence mode="wait">
          {!isSubmitted ? (
            /* ETAPE 1 : SAISIE DE L'EMAIL */
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25 }}
            >
                  {/* SIGNAL D'URGENCE — l'ambre ne figure nulle part ailleurs dans
                      l'application : il marque cette page comme le chemin de
                      déblocage, sans la confondre avec un état d'erreur. */}
              <div className="flex justify-center mb-5">
                <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-200 text-amber-700 text-[11px] font-bold uppercase tracking-wide">
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                  </svg>
                  Accès bloqué
                </span>
              </div>

              {/* HÉROS : anneau pulsé pour attirer l'œil sans clignoter */}
              <div className="flex justify-center mb-4">
                <div className="relative">
                  <span
                    aria-hidden="true"
                    className="absolute inset-0 rounded-full bg-[#209BBF]/20 motion-safe:animate-ping"
                  />
                  <div className="relative w-16 h-16 rounded-full bg-gradient-to-br from-[#1D7893] to-[#209BBF] text-white flex items-center justify-center shadow-lg shadow-[#1D7893]/30">
                    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25l-3 3m0-6.75v-1.5a1.5 1.5 0 013-1.5m0 0V9m0 0V7.5m3 0h6m-3 0V6a3 3 0 00-3-3h-1.5" />
                    </svg>
                  </div>
                </div>
              </div>

              <h1 className="text-2xl font-extrabold text-[#1F3D4D] text-center mb-2">
                Mot de passe oublié ?
              </h1>
              <p className="text-sm text-gray-600 text-center mb-7 leading-relaxed">
                Vous n&apos;accédez plus à vos dossiers ? Déclarez votre demande,
                l&apos;administration vous débloquera.
              </p>

              {/* ÉTAPES NUMÉROTÉES — plus lisible qu'un paragraphe, et ça
                  indique tout de suite que le traitement est humain. */}
              <div className="bg-[#F4FAFC] rounded-2xl border border-[#209BBF]/15 p-4 mb-6">
                <p className="text-[11px] font-extrabold text-[#1D7893] uppercase tracking-wide mb-3">
                  Comment ça marche
                </p>
                <ol className="space-y-2.5">
                  {etapes.map((etape, index) => (
                    <li key={etape} className="flex gap-3 text-[11.5px] text-[#1F3D4D] leading-relaxed">
                      <span className="shrink-0 w-5 h-5 rounded-full bg-[#1D7893] text-white text-[10px] font-bold flex items-center justify-center mt-px">
                        {index + 1}
                      </span>
                      <span>{etape}</span>
                    </li>
                  ))}
                </ol>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="email-reinit" className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">
                    Adresse Email professionnelle
                  </label>
                  <input
                    id="email-reinit"
                    type="email"
                    required
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="dr.medecin@pancreacare.dz"
                    className="w-full px-4 py-3.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm transition-all bg-gray-50/50"
                  />
                </div>

                {error && (
                  <p
                    role="alert"
                    className="text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2"
                  >
                    {error}
                  </p>
                )}

                <motion.button
                  type="submit"
                  disabled={isLoading}
                  whileHover={isLoading ? undefined : { scale: 1.02 }}
                  whileTap={isLoading ? undefined : { scale: 0.98 }}
                  className="w-full py-4 bg-gradient-to-r from-[#1D7893] to-[#209BBF] hover:from-[#1F3D4D] hover:to-[#1D7893] text-white font-bold rounded-xl shadow-lg shadow-[#1D7893]/25 transition-all duration-200 text-sm mt-2 disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {isLoading ? "Envoi en cours…" : "Demander la réinitialisation"}
                </motion.button>
              </form>

              {/* Rappel indispensable : sans email automatique, un médecin
                  qui ne reçoit rien risquerait de conclure que la demande a
                  échoué. */}
              <p className="text-[11px] text-gray-500 text-center mt-5 leading-relaxed">
                Aucun email n&apos;est envoyé automatiquement. Si la situation est
                urgente, appelez l&apos;administration plutôt que d&apos;attendre.
              </p>
            </motion.div>
          ) : (
            /* ETAPE 2 : CONFIRMATION */
            <motion.div
              key="confirmation"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="text-center py-2"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.1, type: "spring", stiffness: 220, damping: 14 }}
                className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-emerald-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-emerald-500/25"
              >
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </motion.div>

              <h2 className="text-xl font-extrabold text-[#1F3D4D] mb-2">
                Demande enregistrée
              </h2>
              <p className="text-xs text-gray-600 mb-6 leading-relaxed">{message}</p>

              {/* « ET MAINTENANT ? » — la demande n'est qu'un début, la
                  question suivante du médecin est toujours « et après ? ». */}
              <div className="text-left bg-[#F4FAFC] rounded-2xl border border-[#209BBF]/15 p-4 mb-5">
                <p className="text-[11px] font-extrabold text-[#1D7893] uppercase tracking-wide mb-3">
                  Et maintenant ?
                </p>
                <ol className="space-y-3">
                  <li className="flex gap-3 text-[11.5px] text-[#1F3D4D] leading-relaxed">
                    <span className="shrink-0 w-5 h-5 rounded-full bg-white border border-[#209BBF]/30 text-[#1D7893] text-[10px] font-bold flex items-center justify-center mt-px">
                      1
                    </span>
                    <span>
                      Votre demande est visible immédiatement par l&apos;administration.
                    </span>
                  </li>
                  <li className="flex gap-3 text-[11.5px] text-[#1F3D4D] leading-relaxed">
                    <span className="shrink-0 w-5 h-5 rounded-full bg-white border border-[#209BBF]/30 text-[#1D7893] text-[10px] font-bold flex items-center justify-center mt-px">
                      2
                    </span>
                    <span>
                      Elle vous contacte et vous transmet un lien, valable une
                      heure et utilisable <strong>une seule fois</strong>.
                    </span>
                  </li>
                  <li className="flex gap-3 text-[11.5px] text-[#1F3D4D] leading-relaxed">
                    <span className="shrink-0 w-5 h-5 rounded-full bg-white border border-[#209BBF]/30 text-[#1D7893] text-[10px] font-bold flex items-center justify-center mt-px">
                      3
                    </span>
                    <span>Vous choisissez un nouveau mot de passe et vous vous connectez.</span>
                  </li>
                </ol>
              </div>

              <div className="p-3.5 bg-amber-50/90 rounded-xl border border-amber-200 text-[11px] text-[#1F3D4D] mb-6 text-left">
                <strong>Restez joignable.</strong> L&apos;administrateur vous
                transmettra le lien par téléphone ou messagerie : aucun email ne
                part de la plateforme.
              </div>

              <button
                onClick={() => setIsSubmitted(false)}
                className="text-xs text-[#209BBF] font-semibold hover:underline"
              >
                Corriger l&apos;adresse ou faire une nouvelle demande
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
