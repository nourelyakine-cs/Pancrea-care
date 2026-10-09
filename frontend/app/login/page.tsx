"use client";

import { Suspense, useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

import {
  DEFAULT_PASSWORD_POLICY,
  TOKEN_KEY,
  getPasswordPolicy,
  login,
  signup,
  type Compte,
  type PasswordPolicy,
} from "@/lib/api";
import PasswordRequirements, { isPasswordCompliant } from "@/components/PasswordRequirements";

import authImg from "@/assets/about-doctors.png"; 
import logoImg from "@/assets/logo.png"; 

/** Espace correspondant au rôle : c'est le compte connecté qui décide, pas
 *  l'écran d'où l'on arrive. Un médecin ne peut donc pas atterrir sur /admin
 *  et un super admin ne reste pas bloqué sur la liste des patients. */
function espacePour(compte: Compte): string {
  return compte.role === "super_admin" ? "/admin" : "/dashboard";
}

function AuthPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(() => searchParams.get("mode") === "signup");
  const [isExiting, setIsExiting] = useState(false);
  const [awaitingValidation, setAwaitingValidation] = useState<{ email: string; message: string } | null>(null);

  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [telephone, setTelephone] = useState("");
  const [hopital, setHopital] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // La garde d'accès renvoie ici avec `?motif=profil-absent` quand la session est
  // valide mais sans profil clinique. Sans ce message, l'utilisateur rejoue sa
  // connexion et repart au même endroit sans jamais comprendre d'où vient le
  // renvoi. Message initialisé une seule fois : il dépend de la redirection,
  // pas de la saisie.
  const [error, setError] = useState(() =>
    searchParams.get("motif") === "profil-absent"
      ? "Votre compte est actif mais pas encore rattaché à un profil clinique. Contactez l'administration de la plateforme pour le rattacher."
      : ""
  );
  const [policy, setPolicy] = useState<PasswordPolicy | null>(null);

  // Les exigences affichées viennent de l'API : c'est exactement ce que le
  // serveur refusera, pas une copie qui pourrait dériver.
  useEffect(() => {
    let active = true;
    getPasswordPolicy().then((p) => {
      if (active) setPolicy(p);
    });
    return () => {
      active = false;
    };
  }, []);

  const passwordCompliant = isPasswordCompliant(password, policy ?? DEFAULT_PASSWORD_POLICY);
  const showSignUpPitch = isSignUp;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSignUp && !passwordCompliant) {
      setError("Le mot de passe ne respecte pas les exigences ci-dessus.");
      return;
    }
    setIsLoading(true);
    setError("");
    try {
      if (isSignUp) {
        const res = await signup({ nom, prenom, email, password, telephone, hopital });
        // Le compte part en file d'attente : aucun jeton n'est renvoyé, il n'y
        // a donc rien à mémoriser ici. On affiche ce que va devenir la
        // connexion au lieu de basculer sur un formulaire inutile.
        setAwaitingValidation({ email, message: res.message });
      } else {
        const session = await login(email, password);
        localStorage.setItem(TOKEN_KEY, session.access_token);
        router.push(espacePour(session.compte));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToHome = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsExiting(true);
    setTimeout(() => {
      router.push("/");
    }, 400);
  };

  if (awaitingValidation) {
    return (
      <ValidationPending
        email={awaitingValidation.email}
        message={awaitingValidation.message}
        onBack={() => {
          setAwaitingValidation(null);
          setIsSignUp(false);
          setError("");
        }}
      />
    );
  }

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
          <Link 
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
          </Link>

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
                      alt="PancreaCare" 
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
                              required
                              maxLength={100}
                              autoComplete="family-name"
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
                              required
                              maxLength={100}
                              autoComplete="given-name"
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
                            maxLength={30}
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
                            maxLength={150}
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
                      required
                      maxLength={255}
                      autoComplete="email"
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
                      required
                      autoComplete={isSignUp ? "new-password" : "current-password"}
                      placeholder="••••••••" 
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                    />
                    {isSignUp && (
                      <PasswordRequirements password={password} policy={policy} className="mt-2" />
                    )}
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
                    disabled={isLoading || (isSignUp && password.length > 0 && !passwordCompliant)}
                    className="w-full py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-300 mt-2 text-xs disabled:opacity-60 disabled:cursor-not-allowed"
                  >
                    {isLoading ? "Veuillez patienter..." : (isSignUp ? "Envoyer ma demande" : "Se connecter")}
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
                alt="Équipe médicale spécialiste du pancréas" 
                fill
                priority
                className="object-cover"
              />

              <div className="absolute inset-0 bg-gradient-to-t from-[#1D7893]/90 via-[#1D7893]/40 to-transparent flex flex-col justify-end p-8 text-white">
                <h3 className="text-xl font-bold mb-2">
                  {showSignUpPitch ? "Rejoignez la plateforme" : "Bienvenue Docteur"}
                </h3>
                <p className="text-xs text-cyan-100 mb-6 leading-relaxed font-light max-w-sm">
                  {showSignUpPitch 
                    ? "Demandez votre accès : un administrateur vérifie chaque inscription avant de l'activer."
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

/**
 * Écran affiché après une inscription.
 *
 * Le compte est en attente de validation : le message dit explicitement que la
 * connexion n'est pas encore possible et pourquoi. Sans cela, le médecin
 * reviendrait sur /login, échouerait, et croirait que la plateforme est
 * cassée au lieu d'être simplement en attente.
 */
function ValidationPending({
  email,
  message,
  onBack,
}: {
  email: string;
  message: string;
  onBack: () => void;
}) {
  return (
    <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50 text-center">
        <div className="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <h2 className="text-xl font-extrabold text-[#1D7893] mb-2">Demande transmise</h2>
        <p className="text-xs text-gray-600 mb-4 leading-relaxed">{message}</p>

        {email && (
          <p className="text-xs text-gray-600 mb-6">
            Adresse déclarée :{" "}
            <span className="font-semibold text-[#1F3D4D]">{email}</span>
          </p>
        )}

        <div className="p-3.5 bg-blue-50/80 rounded-xl border border-blue-100 text-[11px] text-[#1F3D4D] mb-6 text-left">
          <strong>En cas d&apos;oubli de mot de passe :</strong> la plateforme
          n&apos;envoie aucun email. Passez par « Mot de passe oublié » : votre
          demande est transmise à l&apos;administration, qui vous communiquera un
          lien de réinitialisation à usage unique.
        </div>

        <button
          onClick={onBack}
          className="w-full py-3 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-200 text-sm"
        >
          Retour à la connexion
        </button>
      </div>
    </div>
  );
}

export default function AuthPage() {
  return <Suspense fallback={<div className="min-h-screen bg-[#EAF4F7]" />}><AuthPageContent /></Suspense>;
}
