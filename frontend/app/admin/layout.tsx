"use client";

import Image from "next/image";
import Link from "next/link";
import { useGardeAcces } from "@/lib/use-garde-acces";
import logoImg from "@/assets/logo.png";

/**
 * Coquille de l'espace d'administration.
 *
 * Elle n'assure que la garde et l'habillage : la file de validation et les
 * statistiques vivent dans `page.tsx`. Le contrôle effectif du rôle est fait
 * par l'API sur chaque route `/admin/*` — cette garde n'est que le pendant
 * côté interface, pour ne pas afficher un écran vide à quelqu'un qui n'y a pas
 * sa place.
 */
export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { compte, chargement, deconnexion } = useGardeAcces("super_admin");

  if (chargement) {
    return (
      <div className="min-h-screen bg-[#F4F8FA] flex items-center justify-center font-serif">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-[#209BBF]/30 border-t-[#209BBF] rounded-full animate-spin mx-auto" />
          <p className="mt-3 text-xs text-gray-500">Vérification des accès…</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F4F8FA] flex flex-col font-serif">
      <header className="bg-white border-b border-gray-100 px-5 sm:px-8 py-4 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <Image
            src={logoImg}
            alt="PancreaCare"
            width={130}
            height={38}
            className="h-8 w-auto object-contain"
          />
          <span className="hidden sm:inline text-xs font-semibold text-gray-400 border-l border-gray-200 pl-3">
            Administration
          </span>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-xs font-bold text-[#1F3D4D]">
              {compte ? `${compte.prenom} ${compte.nom}` : "Administrateur"}
            </p>
            <p className="text-[10px] text-gray-400">Super administrateur</p>
          </div>

          {/* L'administrateur est aussi praticien : il doit pouvoir passer de
              l'un à l'autre espace sans se déconnecter. */}
          <Link
            href="/dashboard"
            className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-xl bg-[#EAF4F7] text-[#1D7893] text-xs font-semibold hover:bg-[#1D7893] hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>Espace clinique</span>
          </Link>

          <button
            onClick={deconnexion}
            className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-red-500 hover:bg-red-50 rounded-xl transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Se déconnecter</span>
          </button>
        </div>
      </header>

      <main className="flex-1 px-5 sm:px-8 py-6 sm:py-8 overflow-y-auto">{children}</main>
    </div>
  );
}
