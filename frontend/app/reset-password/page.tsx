"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useSearchParams } from "next/navigation";import { motion } from "framer-motion";
import logoImg from "@/assets/logo.png";
import { DEFAULT_PASSWORD_POLICY, getPasswordPolicy, resetPassword, type PasswordPolicy } from "@/lib/api";
import PasswordRequirements, { isPasswordCompliant } from "@/components/PasswordRequirements";

function ResetPasswordContent() {
  const searchParams = useSearchParams();

  // Jeton à usage unique remis par l'administrateur, en paramètre d'URL.
  const jeton = useMemo(() => searchParams.get("jeton") ?? "", [searchParams]);

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [policy, setPolicy] = useState<PasswordPolicy>(DEFAULT_PASSWORD_POLICY);

  useEffect(() => {
    let active = true;
    getPasswordPolicy().then((p) => {
      if (active) setPolicy(p);
    });
    return () => {
      active = false;
    };
  }, []);

  const passwordCompliant = isPasswordCompliant(password, policy);
  const confirmMismatch = confirmPassword.length > 0 && password !== confirmPassword;

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Les deux mots de passe ne correspondent pas.");
      return;
    }
    if (!passwordCompliant) {
      setError("Le mot de passe ne respecte pas les exigences ci-dessous.");
      return;
    }
    setIsLoading(true);
    setError("");
    try {
      await resetPassword(jeton, password);
      setIsSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif">
        <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50 text-center">
          <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-xl font-extrabold text-[#1D7893] mb-2">Mot de passe mis à jour</h2>
          <p className="text-xs text-gray-600 mb-6 leading-relaxed">
            Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.
            Le lien est désormais invalide.
          </p>
          <Link
            href="/login"
            className="inline-block w-full py-3 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all text-sm"
          >
            Se connecter
          </Link>
        </div>
      </div>
    );
  }

  // Aucun jeton : inutile d'afficher un formulaire qui échouerait à l'envoi.
  if (!jeton) {
    return (
      <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif">
        <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50 text-center">
          <div className="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-extrabold text-[#1D7893] mb-2">Lien incomplet</h2>
          <p className="text-xs text-gray-600 mb-6 leading-relaxed">
            Ce lien de réinitialisation ne contient pas de jeton. Demandez-en un
            nouveau à l&apos;administration : elle vous en communiquera un autre.
          </p>
          <Link
            href="/forgot-password"
            className="inline-block w-full py-3 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all text-sm"
          >
            Demander un nouveau lien
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50">
        <div className="flex justify-center mb-6">
          <Image src={logoImg} alt="PANCRA CARE" width={150} height={45} className="h-10 w-auto object-contain" />
        </div>

        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h2 className="text-2xl font-extrabold text-[#1D7893] text-center mb-2">
            Nouveau mot de passe
          </h2>
          <p className="text-xs text-gray-500 text-center mb-6">
            Choisissez votre nouveau mot de passe de connexion.
          </p>

          <form onSubmit={handleReset} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">Nouveau mot de passe</label>
              <input
                type="password"
                required
                autoComplete="new-password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm bg-gray-50/50"
              />
              <PasswordRequirements password={password} className="mt-2" />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#1F3D4D] mb-1.5">Confirmer le mot de passe</label>
              <input
                type="password"
                required
                autoComplete="new-password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                aria-invalid={confirmMismatch}
                className={`w-full px-4 py-3 rounded-xl border focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-sm bg-gray-50/50 ${
                  confirmMismatch ? "border-red-300" : "border-gray-200 focus:border-[#209BBF]"
                }`}
              />
              {confirmMismatch && (
                <p className="mt-1.5 text-[11px] text-red-600">Les deux saisies diffèrent.</p>
              )}
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
        </motion.div>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#EAF4F7]" />}>
      <ResetPasswordContent />
    </Suspense>
  );
}