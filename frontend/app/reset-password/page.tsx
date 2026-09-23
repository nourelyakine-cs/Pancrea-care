"use client";

import { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import logoImg from "@/assets/logo.png";
import { resetPassword } from "@/lib/api";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [tokens] = useState(() => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return {
      access_token: params.get("access_token") ?? "",
      refresh_token: params.get("refresh_token") ?? "",
    };
  });

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Les deux mots de passe ne correspondent pas.");
      return;
    }
    if (!tokens.access_token || !tokens.refresh_token) {
      setError("Lien de réinitialisation invalide ou expiré. Relancez la procédure.");
      return;
    }
    setIsLoading(true);
    setError("");
    try {
      await resetPassword(tokens.access_token, tokens.refresh_token, password);
      setIsSuccess(true);
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50">
        
        <div className="flex justify-center mb-6">
          <Image src={logoImg} alt="PANCRA CARE" width={150} height={45} className="h-10 w-auto object-contain" />
        </div>

        {!isSuccess ? (
          <div>
            <h2 className="text-2xl font-extrabold text-[#1D7893] text-center mb-2">
              Nouveau mot de passe
            </h2>
            <p className="text-xs text-gray-500 text-center mb-6">
              Saisissez votre nouveau mot de passe de connexion.
            </p>

            <form onSubmit={handleReset} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">Nouveau mot de passe</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm bg-gray-50/50"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">Confirmer le mot de passe</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm bg-gray-50/50"
                />
              </div>

              {error && (
                  <p className="text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
                    {error}
                  </p>
                )}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3.5 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all text-sm mt-2 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {isLoading ? "Mise à jour en cours..." : "Mettre à jour le mot de passe"}
              </button>
            </form>
          </div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-4">
            <div className="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-3">
              ✓
            </div>
            <h3 className="text-lg font-bold text-[#1D7893] mb-1">Mot de passe modifié !</h3>
            <p className="text-xs text-gray-500">Redirection automatique vers la page de connexion...</p>
          </motion.div>
        )}

      </div>
    </div>
  );
}