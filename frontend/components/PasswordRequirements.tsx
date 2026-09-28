"use client";

import { useEffect, useState } from "react";

import {
  DEFAULT_PASSWORD_POLICY,
  getPasswordPolicy,
  type PasswordPolicy,
} from "@/lib/api";

interface Rule {
  id: "min_length" | "lowercase" | "uppercase" | "digit";
  label: string;
  satisfied: boolean;
}

function buildRules(password: string, policy: PasswordPolicy): Rule[] {  const rules: Rule[] = [
    {
      id: "min_length",
      label: `Au moins ${policy.min_length} caractères`,
      satisfied: password.length >= policy.min_length,
    },
  ];
  if (policy.require_lowercase) {
    rules.push({ id: "lowercase", label: "Une lettre minuscule (a-z)", satisfied: /[a-z]/.test(password) });
  }
  if (policy.require_uppercase) {
    rules.push({ id: "uppercase", label: "Une lettre majuscule (A-Z)", satisfied: /[A-Z]/.test(password) });
  }
  if (policy.require_digit) {
    rules.push({ id: "digit", label: "Un chiffre (0-9)", satisfied: /[0-9]/.test(password) });
  }
  return rules;
}

/** `true` si le mot de passe satisfait toutes les règles de la politique. */
export function isPasswordCompliant(password: string, policy: PasswordPolicy): boolean {
  return buildRules(password, policy).every((rule) => rule.satisfied);
}

/**
 * Liste des exigences du mot de passe, avec validation en direct.
 *
 * Les règles proviennent de l'API (`GET /auth/password-policy`) pour rester
 * alignées sur ce que le serveur accepte réellement. Si l'API est injoignable,
 * on retombe sur la politique par défaut plutôt que d'afficher un formulaire muet.
 */
export default function PasswordRequirements({
  password,
  policy,
  className = "",
}: {
  password: string;
  policy?: PasswordPolicy | null;
  className?: string;
}) {
  const [fetchedPolicy, setFetchedPolicy] = useState<PasswordPolicy | null>(null);

  useEffect(() => {
    if (policy) return;
    let active = true;
    getPasswordPolicy().then((p) => {
      if (active) setFetchedPolicy(p);
    });
    return () => {
      active = false;
    };
  }, [policy]);

  const resolved = policy ?? fetchedPolicy ?? DEFAULT_PASSWORD_POLICY;
  const rules = buildRules(password, resolved);
  const remaining = rules.filter((rule) => !rule.satisfied).length;

  return (
    <div className={`rounded-xl border border-gray-100 bg-gray-50/60 px-3 py-2.5 ${className}`}>
      <p className="text-[11px] font-semibold text-[#1F3D4D] mb-1.5">
        {password.length === 0
          ? "Exigences du mot de passe"
          : remaining === 0
            ? "Mot de passe conforme"
            : `Il manque ${remaining} exigence${remaining > 1 ? "s" : ""}`}
      </p>
      <ul className="space-y-1">
        {rules.map((rule) => (
          <li
            key={rule.id}
            className={`flex items-center gap-1.5 text-[11px] transition-colors ${
              rule.satisfied ? "text-emerald-700" : "text-gray-500"
            }`}
          >
            <span
              aria-hidden="true"
              className={`flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full text-[9px] font-bold ${
                rule.satisfied ? "bg-emerald-100 text-emerald-700" : "bg-gray-200 text-gray-400"
              }`}
            >
              {rule.satisfied ? "✓" : "•"}
            </span>
            <span className={rule.satisfied ? "line-through opacity-70" : ""}>{rule.label}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
