"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import logoImg from "@/assets/logo.png";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      // Ici vous ajouterez l'appel API (ex: Supabase, Firebase ou votre backend)
      setIsSubmitted(true);
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif relative">
      
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

      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50">
        
        {/* LOGO */}
        <div className="flex justify-center mb-6">
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
              <h2 className="text-2xl font-extrabold text-[#1D7893] text-center mb-2">
                Mot de passe oublié ?
              </h2>
              <p className="text-xs text-gray-500 text-center mb-6 leading-relaxed">
                Entrez votre adresse email professionnelle. Nous vous enverrons un lien sécurisé pour réinitialiser votre accès.
              </p>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">Adresse Email</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="dr.medecin@pancreacare.dz"
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm transition-all bg-gray-50/50"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-3.5 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-200 text-sm mt-2"
                >
                  Envoyer le lien de réinitialisation
                </button>
              </form>
            </motion.div>
          ) : (
            /* ETAPE 2 : CARTE DE CONFIRMATION (PLAQUE) */
            <motion.div
              key="confirmation"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="text-center py-2"
            >
              {/* ICONE EMAIL DYNAMIQUE */}
              <div className="w-16 h-16 bg-cyan-100 text-[#1D7893] rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 002-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>

              <h3 className="text-xl font-bold text-[#1D7893] mb-2">Vérifiez votre boîte mail</h3>
              <p className="text-xs text-gray-600 mb-6 leading-relaxed">
                Un e-mail contenant le lien de réinitialisation a été envoyé à <br />
                <span className="font-semibold text-[#1F3D4D]">{email}</span>.
              </p>

              <div className="p-3.5 bg-blue-50/80 rounded-xl border border-blue-100 text-[11px] text-[#1D7893] mb-6 text-left">
                💡 <strong>Conseil :</strong> Pensez à vérifier votre dossier de courriers indésirables (Spam) si vous ne trouvez pas l'email.
              </div>

              <button
                onClick={() => setIsSubmitted(false)}
                className="text-xs text-[#209BBF] font-semibold hover:underline"
              >
                Renvoyer l'email ou changer d'adresse
              </button>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  );
}