"use client";

import { useCallback, useEffect, useState } from "react";
import {
  accepterCompte,
  bloquerCompte,
  cloturerDemandeReinitialisation,
  debloquerCompte,
  definirMotDePasseTemporaire,
  genererLienReinitialisation,
  getAdminComptes,
  getAdminStatistiques,
  getDemandesReinitialisation,
  type CompteAdmin,
  type DemandeReinitialisation,
  type StatistiquesAdmin,
  type StatutCompte,
} from "@/lib/api";

type Onglet = "comptes" | "demandes";

const LIBELLE_STATUT: Record<StatutCompte, string> = {
  en_attente: "En attente",
  actif: "Actif",
  bloque: "Bloqué",
};

const COULEUR_STATUT: Record<StatutCompte, string> = {
  en_attente: "bg-amber-100 text-amber-700",
  actif: "bg-emerald-100 text-emerald-700",
  bloque: "bg-red-100 text-red-700",
};

function formatDate(v: string | null): string {
  if (!v) return "—";
  return new Date(v).toLocaleString("fr-FR", { dateStyle: "short", timeStyle: "short" });
}

/** Copie dans le presse-papiers avec repli sur les navigateurs anciens :
 *  `navigator.clipboard` est absent en HTTP simple, ce qui est courant en
 *  développement local. Sans repli, l'admin ne pourrait pas récupérer le lien. */
async function copier(texte: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(texte);
    return true;
  } catch {
    return false;
  }
}

export default function AdminPage() {
  const [onglet, setOnglet] = useState<Onglet>("comptes");

  const [stats, setStats] = useState<StatistiquesAdmin | null>(null);
  const [comptes, setComptes] = useState<CompteAdmin[]>([]);
  const [demandes, setDemandes] = useState<DemandeReinitialisation[]>([]);

  const [filtre, setFiltre] = useState<StatutCompte | "tous">("en_attente");
  const [recherche, setRecherche] = useState("");

  const [actionEnCours, setActionEnCours] = useState<string | null>(null);
  const [erreur, setErreur] = useState("");
  const [lien, setLien] = useState<{ url: string; expire_le: string } | null>(null);
  const [copie, setCopie] = useState(false);

  // Les trois lectures partagent une seule requête groupée, et une seule
  // temporisation : avec un effet par critère, changer le filtre relançait
  // aussi la recherche, et chaque frappe déclenchait deux requêtes.
  const charger = useCallback(
    async (statut: StatutCompte | "tous", rechercheCourante: string) => {
      try {
        const [s, c, d] = await Promise.all([
          getAdminStatistiques(),
          getAdminComptes({
            statut: statut === "tous" ? undefined : statut,
            recherche: rechercheCourante.trim() || undefined,
          }),
          getDemandesReinitialisation("en_attente"),
        ]);
        setStats(s);
        setComptes(c);
        setDemandes(d);
        setErreur("");
      } catch (err) {
        setErreur(err instanceof Error ? err.message : "Impossible de charger les données.");
      }
    },
    [],
  );

  // L'état est lu au moment du rendu, et la requête part 350 ms plus tard :
  // `charger` reste stable, donc une seule frappe = une seule requête.
  useEffect(() => {
    const t = setTimeout(() => void charger(filtre, recherche), 350);
    return () => clearTimeout(t);
  }, [filtre, recherche, charger]);

  /** Enveloppe commune : bloque les doubles clics et affiche l'échec sans
   *  laisser l'interface dans un état intermédiaire trompeur. */
  const executer = async (cle: string, action: () => Promise<unknown>) => {
    setActionEnCours(cle);
    setErreur("");
    try {
      await action();
      // On relit avec les critères affichés à l'instant : le médecin a peut-être
      // tapé une recherche que la temporisation n'a pas encore envoyée.
      await charger(filtre, recherche);
    } catch (err) {
      setErreur(err instanceof Error ? err.message : "L'opération a échoué.");
    } finally {
      setActionEnCours(null);
    }
  };

  const cartes = stats
    ? [
        { label: "Comptes totaux", valeur: stats.total_comptes, accent: "text-[#1F3D4D]" },
        { label: "Actifs", valeur: stats.comptes_actifs, accent: "text-emerald-600" },
        { label: "En attente", valeur: stats.comptes_en_attente, accent: "text-amber-600" },
        { label: "Bloqués", valeur: stats.comptes_bloques, accent: "text-red-600" },
        { label: "Demandes de réinit.", valeur: stats.demandes_reinitialisation_en_attente, accent: "text-[#1D7893]" },
        { label: "Comptes actifs (7 j)", valeur: stats.connexions_7_jours, accent: "text-[#1F3D4D]" },
      ]
    : [];

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-[#1D7893]">Administration des comptes</h1>
        <p className="text-xs text-gray-500 mt-1">
          Validez les inscriptions, gérez les accès et traitez les demandes de réinitialisation.
        </p>
      </div>

      {erreur && (
        <p className="text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-xl px-3 py-2">
          {erreur}
        </p>
      )}

      {/* STATISTIQUES */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {cartes.length === 0
          ? Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-20 bg-white rounded-2xl border border-gray-100 animate-pulse" />
            ))
          : cartes.map((c) => (
              <div key={c.label} className="bg-white rounded-2xl border border-gray-100 p-4 shadow-sm">
                <p className="text-[10px] uppercase tracking-wide text-gray-400">{c.label}</p>
                <p className={`text-2xl font-extrabold mt-1 ${c.accent}`}>{c.valeur}</p>
              </div>
            ))}
      </div>

      {/* ONGLETS */}
      <div className="flex gap-2 border-b border-gray-200">
        {(
          [
            ["comptes", `Comptes${stats && stats.comptes_en_attente > 0 ? ` (${stats.comptes_en_attente})` : ""}`],
            ["demandes", `Demandes de réinitialisation${stats && stats.demandes_reinitialisation_en_attente > 0 ? ` (${stats.demandes_reinitialisation_en_attente})` : ""}`],
          ] as [Onglet, string][]
        ).map(([id, label]) => (
          <button
            key={id}
            onClick={() => setOnglet(id)}
            className={`px-4 py-2.5 text-xs font-semibold border-b-2 -mb-px transition-colors ${
              onglet === id
                ? "border-[#1D7893] text-[#1D7893]"
                : "border-transparent text-gray-400 hover:text-gray-600"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {onglet === "comptes" ? (
        <section className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              type="search"
              value={recherche}
              onChange={(e) => setRecherche(e.target.value)}
              placeholder="Rechercher un nom ou un email…"
              className="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 bg-white text-sm outline-none focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20"
            />
            <div className="flex gap-2">
              {(["tous", "en_attente", "actif", "bloque"] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setFiltre(s)}
                  className={`px-3 py-2 rounded-xl text-xs font-semibold transition-colors ${
                    filtre === s ? "bg-[#1D7893] text-white" : "bg-white text-gray-500 border border-gray-200 hover:bg-gray-50"
                  }`}
                >
                  {s === "tous" ? "Tous" : LIBELLE_STATUT[s]}
                </button>
              ))}
            </div>
          </div>

          {comptes.length === 0 ? (
            <p className="text-xs text-gray-400 bg-white rounded-2xl border border-gray-100 p-8 text-center">
              Aucun compte ne correspond à ces critères.
            </p>
          ) : (
            <ul className="space-y-3">
              {comptes.map((c) => (
                <li key={c.id_compte} className="bg-white rounded-2xl border border-gray-100 p-4 sm:p-5 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <p className="text-sm font-bold text-[#1F3D4D]">
                          Dr. {c.prenom} {c.nom}
                        </p>
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${COULEUR_STATUT[c.statut]}`}>
                          {LIBELLE_STATUT[c.statut]}
                        </span>
                        {c.role === "super_admin" && (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#EAF4F7] text-[#1D7893]">
                            Administrateur
                          </span>
                        )}
                        {c.doit_changer_mdp && (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-purple-100 text-purple-700">
                            Mot de passe à changer
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{c.email}</p>
                      <p className="text-[10px] text-gray-400 mt-0.5">
                        {c.hopital || "Hôpital non précisé"}
                        {c.telephone ? ` · ${c.telephone}` : ""} · inscrit le {formatDate(c.date_creation)}
                        {c.date_derniere_connexion ? ` · dernière connexion ${formatDate(c.date_derniere_connexion)}` : ""}
                      </p>
                      {c.motif_blocage && (
                        <p className="text-[10px] text-red-500 mt-1">Motif du blocage : {c.motif_blocage}</p>
                      )}
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {c.statut === "en_attente" && (
                        <button
                          onClick={() => executer(`accepter-${c.id_compte}`, () => accepterCompte(c.id_compte))}
                          disabled={actionEnCours !== null}
                          className="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold disabled:opacity-50"
                        >
                          {actionEnCours === `accepter-${c.id_compte}` ? "Validation…" : "Valider"}
                        </button>
                      )}
                      {c.statut === "bloque" && (
                        <button
                          onClick={() => executer(`debloquer-${c.id_compte}`, () => debloquerCompte(c.id_compte))}
                          disabled={actionEnCours !== null}
                          className="px-3 py-2 rounded-xl bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold disabled:opacity-50"
                        >
                          Débloquer
                        </button>
                      )}
                      {c.statut !== "en_attente" && c.role === "medecin" && (
                        <button
                          onClick={() => executer(`bloquer-${c.id_compte}`, () => bloquerCompte(c.id_compte))}
                          disabled={actionEnCours !== null}
                          className="px-3 py-2 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 text-xs font-semibold disabled:opacity-50"
                        >
                          Bloquer
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Mot de passe provisoire : dernier recours quand le médecin est
                      injoignable. La plateforme n'envoie aucun email, c'est donc
                      parfois le seul moyen de lui rendre l'accès. */}
                  {c.statut === "bloque" && c.role === "medecin" && (
                    <details className="mt-3">
                      <summary className="text-[11px] text-gray-400 cursor-pointer hover:text-[#1D7893]">
                        Définir un mot de passe provisoire
                      </summary>
                      <FormulaireMotDePasse
                        onSubmit={(mdp) =>
                          executer(`mdp-${c.id_compte}`, () => definirMotDePasseTemporaire(c.id_compte, mdp))
                        }
                        enCours={actionEnCours === `mdp-${c.id_compte}`}
                      />
                    </details>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>
      ) : (
        <section className="space-y-3">
          {demandes.length === 0 ? (
            <p className="text-xs text-gray-400 bg-white rounded-2xl border border-gray-100 p-8 text-center">
              Aucune demande en attente.
            </p>
          ) : (
            <ul className="space-y-3">
              {demandes.map((d) => (
                <li key={d.id_demande} className="bg-white rounded-2xl border border-gray-100 p-4 sm:p-5 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-[#1F3D4D]">
                        Dr. {d.prenom} {d.nom}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">{d.email}</p>
                      <p className="text-[10px] text-gray-400 mt-0.5">
                        Demandée le {formatDate(d.date_demande)}
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() =>
                          executer(`lien-${d.id_demande}`, async () => {
                            const res = await genererLienReinitialisation(d.id_demande);
                            setLien({ url: res.lien, expire_le: res.expire_le });
                            setCopie(false);
                          })
                        }
                        disabled={actionEnCours !== null}
                        className="px-3 py-2 rounded-xl bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold disabled:opacity-50"
                      >
                        {actionEnCours === `lien-${d.id_demande}` ? "Génération…" : "Générer le lien"}
                      </button>
                      <button
                        onClick={() =>
                          executer(`annuler-${d.id_demande}`, () =>
                            cloturerDemandeReinitialisation(d.id_demande, "annulee"),
                          )
                        }
                        disabled={actionEnCours !== null}
                        className="px-3 py-2 rounded-xl border border-gray-200 text-gray-500 hover:bg-gray-50 text-xs font-semibold disabled:opacity-50"
                      >
                        Refuser
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}

      {/* LIEN GÉNÉRÉ : affiché explicitement plutôt que copié « dans le vide ».
      La plateforme n'a pas d'email : c'est l'admin qui le transmet. */}
      {lien && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="w-full max-w-lg bg-white rounded-3xl shadow-2xl p-6 sm:p-8">
            <h2 className="text-lg font-extrabold text-[#1D7893] mb-2">Lien de réinitialisation</h2>
            <p className="text-xs text-gray-500 mb-4">
              Communiquez ce lien au médecin par téléphone ou messagerie. Il est
              à usage unique et expire le {formatDate(lien.expire_le)}.
            </p>
            <div className="flex gap-2">
              <input
                readOnly
                value={lien.url}
                onFocus={(e) => e.currentTarget.select()}
                className="flex-1 px-3 py-2.5 rounded-xl border border-gray-200 bg-gray-50 text-[11px] font-mono outline-none"
              />
              <button
                onClick={async () => {
                  const ok = await copier(lien.url);
                  if (ok) {
                    setCopie(true);
                    setTimeout(() => setCopie(false), 2500);
                  }
                }}
                className="px-4 py-2.5 rounded-xl bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold shrink-0"
              >
                {copie ? "Copié ✓" : "Copier"}
              </button>
            </div>
            {!copie && (
              <p className="text-[10px] text-amber-600 mt-2">
                Si la copie automatique échoue (connexion non sécurisée), sélectionnez le lien et copiez-le manuellement.
              </p>
            )}
            <button
              onClick={() => setLien(null)}
              className="mt-6 w-full py-2.5 rounded-xl border border-gray-200 text-gray-600 text-xs font-semibold hover:bg-gray-50"
            >
              Fermer
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/** Saisie du mot de passe provisoire. Le contrôle de robustesse est appliqué
 *  côté serveur ; l'indiquer ici évite un aller-retour pour une règle évidente. */
function FormulaireMotDePasse({
  onSubmit,
  enCours,
}: {
  onSubmit: (motDePasse: string) => Promise<void>;
  enCours: boolean;
}) {
  const [mdp, setMdp] = useState("");

  const assezSolide =
    mdp.length >= 8 && /[a-z]/.test(mdp) && /[A-Z]/.test(mdp) && /[0-9]/.test(mdp);

  return (
    <div className="flex flex-col sm:flex-row gap-2 mt-2">
      <input
        type="text"
        value={mdp}
        onChange={(e) => setMdp(e.target.value)}
        placeholder="8 caractères, majuscule, minuscule et chiffre"
        className="flex-1 px-3 py-2 rounded-xl border border-gray-200 bg-gray-50 text-xs outline-none focus:border-[#209BBF]"
      />
      <button
        onClick={() => onSubmit(mdp)}
        disabled={!assezSolide || enCours}
        className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold disabled:opacity-50"
      >
        {enCours ? "Définition…" : "Définir"}
      </button>
    </div>
  );
}
