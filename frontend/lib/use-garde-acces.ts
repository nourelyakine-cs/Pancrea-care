"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { TOKEN_KEY, clearToken, getCurrentSession, type Compte, type MedecinProfile } from "@/lib/api";

export interface EtatSession {
  compte: Compte | null;
  medecin: MedecinProfile | null;
  chargement: boolean;
}

/**
 * Garde d'accès partagée par /dashboard et /admin.
 *
 * L'API refait déjà le contrôle à chaque requête (statut du compte vérifié en
 * base), mais l'interface doit aussi réagir : sans cela, un médecin bloqué
 * continuerait de voir un tableau de bord vide, et un compte déconnecté
 * resterait sur un écran qui ne se recharge plus.
 *
 * `exiger` indique l'espace demandé. Les rôles ne sont pas exclusifs : un
 * administrateur est aussi un praticien, il accède donc aux DEUX espaces. Le
 * contrôle porte sur la présence d'un profil clinique, pas sur le rôle — c'est
 * ce profil qui conditionne l'accès aux données patients.
 */
export function useGardeAcces(exiger: "medecin" | "super_admin"): EtatSession & { deconnexion: () => void } {
  const router = useRouter();
  const [compte, setCompte] = useState<Compte | null>(null);
  const [medecin, setMedecin] = useState<MedecinProfile | null>(null);
  const [chargement, setChargement] = useState(true);

  useEffect(() => {
    // Aucun jeton : inutile d'appeler l'API, elle ne répondrait pas mieux.
    if (typeof window !== "undefined" && !localStorage.getItem(TOKEN_KEY)) {
      router.replace("/login");
      return;
    }

    let actif = true;
    getCurrentSession()
      .then((session) => {
        if (!actif) return;
        setCompte(session.compte);
        setMedecin(session.medecin);

        if (exiger === "super_admin" && session.compte.role !== "super_admin") {
          // Un médecin n'a rien à faire dans la file de validation.
          router.replace("/dashboard");
          return;
        }
        if (exiger === "medecin" && !session.medecin) {
          // Compte sans profil clinique : /dashboard ne lui afficherait que des
          // écrans vides. Un compte en attente n'a pas encore de profil — d'où
          // l'aiguillage vers la connexion, qui explique la raison du refus.
          router.replace("/login?motif=profil-absent");
        }
      })
      .catch(() => {
        // Jeton expiré, révoqué ou compte supprimé : le garder ne sert à rien.
        clearToken();
        router.replace("/login");
      })
      .finally(() => {
        if (actif) setChargement(false);
      });

    return () => {
      actif = false;
    };
  }, [exiger, router]);

  const deconnexion = () => {
    // Sans cette purge, le jeton resterait valide dans le navigateur : le
    // bouton « Se déconnecter » ne servirait à rien.
    clearToken();
    router.replace("/login");
  };

  return { compte, medecin, chargement, deconnexion };
}
