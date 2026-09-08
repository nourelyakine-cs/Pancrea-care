"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

import { login, signup } from "@/lib/api";

import authImg from "@/assets/about-doctors.png"; 
import logoImg from "@/assets/logo.png"; 

export default function AuthPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(false);
  const [isExiting, setIsExiting] = useState(false);

  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [telephone, setTelephone] = useState("");
  const [hopital, setHopital] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      if (isSignUp) {
        const res = await signup({ nom, prenom, email, password, telephone, hopital });
        router.push(res.need_email_confirmation ? "/login?mode=confirm" : "/login");
      } else {
        const { access_token } = await login(email, password);
        localStorage.setItem("token", access_token);
        router.push("/dashboard");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (searchParams.get("mode") === "signup") {
      setIsSignUp(true);
    }
  }, [searchParams]);

  const handleBackToHome = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsExiting(true);
    setTimeout(() => {
      router.push("/");
    }, 400);
  };

  return (
    <AnimatePresence mode="wait">
      {!isExiting && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.96, y: 15 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 md:p-8 font-serif relative"
        >
          {/* BOUTON RETOUR À L'ACCUEIL */}
          <a 
            href="/" 
            onClick={handleBackToHome}
            className="absolute top-6 left-6 z-50"
          >
            <motion.div
              whileHover={{ x: -6 }}
              whileTap={{ scale: 0.9 }}
              transition={{ type: "spring", stiffness: 400, damping: 25 }}
              className="flex items-center gap-2 text-sm font-semibold text-[#1D7893] hover:text-[#209BBF] transition-colors duration-200 cursor-pointer"
            >
              <motion.svg 
                className="w-5 h-5 stroke-current" 
                fill="none" 
                viewBox="0 0 24 24" 
                strokeWidth="2.5" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
              </motion.svg>
            </motion.div>
          </a>

          {/* CONTENEUR PRINCIPAL */}
          <div className="relative w-full max-w-4xl min-h-[600px] max-h-[90vh] bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
            
            {/* SECTION FORMULAIRE (CENTRÉ DYNAMIKEMENT) */}
            <motion.div 
              key={isSignUp ? "signup-form" : "login-form"}
              initial={{ opacity: 0, x: isSignUp ? 50 : -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={`w-full md:w-1/2 h-full p-6 sm:p-8 md:p-10 flex flex-col overflow-y-auto ${
                isSignUp ? "justify-start md:order-2" : "justify-center md:order-1"
              }`}
            >
              <div className="max-w-md mx-auto w-full my-auto flex flex-col justify-center">
                
                {/* LOGO (CONNEXION SEULEMENT) */}
                {!isSignUp && (
                  <Link href="/" className="mb-4 flex justify-center">
                    <Image 
                      src={logoImg} 
                      alt="PANCRA CARE Logo" 
                      width={150} 
                      height={45}
                      className="h-11 w-auto object-contain mx-auto"
                    />
                  </Link>
                )}

                {/* EN-TÊTE DU FORMULAIRE */}
                <div className="mb-5 text-center w-full">
                  <h2 className="text-xl sm:text-2xl font-extrabold text-[#1D7893]">
                    {isSignUp ? "Créer un compte Médecin" : "Espace Médecin"}
                  </h2>
                  <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                    {isSignUp 
                      ? "Rejoignez la plateforme déterministe d'aide à la décision." 
                      : "Veuillez vous identifier pour accéder au suivi patient."}
                  </p>
                </div>

                {/* FORMULAIRE */}
                <form onSubmit={handleSubmit} className="space-y-3 w-full">
                  
                  <AnimatePresence>
                    {isSignUp && (
                      <motion.div 
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-3"
                      >
                        <div className="grid grid-cols-2 gap-2">
                          <div>
                            <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Nom</label>
                            <input 
                              type="text" 
                              placeholder="Benali" 
                              value={nom}
                              onChange={(e) => setNom(e.target.value)}
                              className="w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                            />
                          </div>
                          <div>
                            <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Prénom</label>
                            <input 
                              type="text" 
                              placeholder="Sofiane" 
                              value={prenom}
                              onChange={(e) => setPrenom(e.target.value)}
                              className="w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Numéro de téléphone</label>
                          <input 
                            type="text" 
                            placeholder="0598765432" 
                            value={telephone}
                            onChange={(e) => setTelephone(e.target.value)}
                            className="w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                          />
                        </div>

                        <div>
                          <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Établissement / Hôpital</label>
                          <input 
                            type="text" 
                            placeholder="EHS Aïn Taya" 
                            value={hopital}
                            onChange={(e) => setHopital(e.target.value)}
                            className="w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                          />
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  <div>
                    <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Adresse Email</label>
                    <input 
                      type="email" 
                      placeholder="medecin@pancreacare.dz" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-semibold text-[#1F3D4D] mb-1">Mot de passe</label>
                    <input 
                      type="password" 
                      placeholder="••••••••" 
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                    />
                  </div>

                  {!isSignUp && (
                    <div className="text-right pt-0.5">
                      <Link href="/forgot-password" className="text-[11px] text-[#209BBF] hover:underline font-medium">
                        Mot de passe oublié ?
                      </Link>
                    </div>
                  )}

                  {error && (
                    <p className="text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
                      {error}
                    </p>
                  )}

                  <button 
                    type="submit" 
                    disabled={isLoading}
                    className="w-full py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-300 mt-2 text-xs disabled:opacity-60 disabled:cursor-not-allowed"
                  >
                    {isLoading ? "Veuillez patienter..." : (isSignUp ? "Créer mon compte" : "Se connecter")}
                  </button>
                </form>

                <div className="mt-4 text-center text-xs text-gray-600 md:hidden">
                  {isSignUp ? "Déjà un compte ?" : "Pas encore de compte ?"} {" "}
                  <button 
                    onClick={() => setIsSignUp(!isSignUp)} 
                    className="text-[#1D7893] font-bold underline ml-1"
                  >
                    {isSignUp ? "Se connecter" : "S'inscrire"}
                  </button>
                </div>

              </div>
            </motion.div>

            {/* SECTION PHOTO */}
            <motion.div 
              layout
              transition={{ duration: 0.6, ease: "easeInOut" }}
              className={`hidden md:block w-1/2 min-h-[600px] relative overflow-hidden ${
                isSignUp ? "md:order-1" : "md:order-2"
              }`}
            >
              <Image 
                src={authImg} 
                alt="Authentification Médicale PancreaCare" 
                fill
                priority
                className="object-cover"
              />

              <div className="absolute inset-0 bg-gradient-to-t from-[#1D7893]/90 via-[#1D7893]/40 to-transparent flex flex-col justify-end p-8 text-white">
                <h3 className="text-xl font-bold mb-2">
                  {isSignUp ? "Rejoignez l'équipe" : "Bienvenue Docteur"}
                </h3>
                <p className="text-xs text-cyan-100 mb-6 leading-relaxed font-light max-w-sm">
                  {isSignUp 
                    ? "Créez votre accès sécurisé pour exploiter nos algorithmes décisionnels basés sur les guides cliniques."
                    : "Accédez instantanément aux dossiers patients, à l'historique et aux recommandations thérapeutiques."}
                </p>

                <button 
                  onClick={() => setIsSignUp(!isSignUp)}
                  className="w-fit px-5 py-2 border border-white/80 rounded-full text-xs font-semibold backdrop-blur-sm hover:bg-white hover:text-[#1D7893] transition-all duration-300 shadow-sm"
                >
                  {isSignUp ? "Déjà inscrit ? Se connecter" : "Pas de compte ? S'inscrire"}
                </button>
              </div>
            </motion.div>

          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}