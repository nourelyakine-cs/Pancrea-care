"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { getPatientDetail, getPatients, type PatientDetail } from "@/lib/api";

export interface PatientData {
  // A.1 Démographie
  id: string;
  nom: string;
  prenom: string;
  telephone: string;
  adresse: string;
  dateNaissance: string;
  sexe: "M" | "F";
  age: number;

  // A.2 État Clinique
  ecog?: number;
  etatNutritionnel?: string;
  comorbiditesLourdes?: boolean;
  comorbidites?: string[];
  douleur?: "absente" | "présente";
  intensiteDouleur?: number;
  ictere?: boolean;
  angiocholite?: boolean;
  diabete?: string;
  cholestase?: boolean;
  patientNonOperable?: boolean;

  // A.3 Biologie
  ca199?: number;
  ca199MultipleLsn?: number;
  bilirubine?: number;
  lsnBilirubine?: number;
  bilirubineRatioLsn?: number;
  statutDpd?: string;
  albuminemie?: number;

  // A.4 Imagerie
  localisationTumorale?: string;
  tailleTumorale?: number;
  contactAms?: string;
  contactTroncCoeliaque?: string;
  contactAhc?: string;
  contactVmsVp?: string;
  adenopathieRegionale?: boolean;
  adenopathieDistance?: boolean;
  metastases?: boolean;
  siteMetastases?: string[];

  // TNM
  categorieT?: string;
  categorieN?: string;
  categorieM?: string;
  stadeGlobal?: string;
  resecabilite?: string;

  // A.6 Histologie & Biologie Moléculaire
  preuveHistologique?: boolean;
  statutBrca?: string;
  statutKras?: string;
  statutMsiDmmr?: string;
  fusionNtrk?: string;
  fusionNrg1?: string;

  // A.7 Parcours Thérapeutique
  ligneTraitementActuelle?: number;
  reponseTraitementPrecedent?: string;
  traitementsRecusTexte?: string;
  traitementsRecus?: string[];
  lignePrecedente?: string;
  dureeChimiotherapieMois?: number;
  tumeurControle?: boolean;
  nouvellesMetastases?: boolean;
  chirurgieDembleePrevue?: boolean;
  traitementMedicalPrevu?: boolean;
  pasDeProgressionApres16SemainesPlatine?: boolean;
  toxiciteResiduelle?: boolean;
  detailsToxicite?: string;
}

function computeAge(dateNaissance: string): number {
  const birth = new Date(dateNaissance);
  if (Number.isNaN(birth.getTime())) return 0;
  const now = new Date();
  let age = now.getFullYear() - birth.getFullYear();
  const m = now.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) age -= 1;
  return age;
}

function formatDateNaissance(value: string | null): string {
  if (!value) return "";
  return value.split("T")[0];
}

// Valeurs backend (enums PostgreSQL) -> libellés lisibles dans la modale.
const ENUM_LABELS: Record<string, Record<string, string>> = {
  etatNutritionnel: {
    normal: "Normal",
    denutrition_moderee: "Dénutrition modérée",
    denutrition_severe: "Dénutrition sévère",
    inconnu: "Inconnu",
  },
  diabete: {
    absent: "Absent",
    recent_moins_2ans: "Récent (< 2 ans)",
    ancien: "Ancien",
    inconnu: "Inconnu",
  },
  statutDpd: {
    normal: "Normal",
    deficit_partiel: "Déficit partiel",
    deficit_complet: "Déficit complet",
    non_teste: "Non testé",
  },
  localisationTumorale: {
    tete_crochet: "Tête / Crochet",
    corps_queue: "Corps / Queue",
    inconnu: "Inconnue",
  },
  contact: { absent: "Pas de contact", lt180: "< 180°", ge180: ">= 180°" },
  contactAhc: {
    absent: "Pas de contact",
    court_sans_envahissement: "Court reconstructible",
    envahissant: "Envahissant (non reconstructible)",
  },
  contactVmsVp: {
    absent: "Pas de contact",
    lt180_sans_irregularite: "< 180° sans irrégularité",
    ge180_ou_irregularite: ">= 180° ou irrégularité",
    occlusion_reconstructible: "Occlusion reconstructible",
    occlusion_non_reconstructible: "Occlusion non reconstructible",
  },
  statutBrca: { mute: "Muté", non_mute: "Non muté", non_teste: "Non testé" },
  statutKras: {
    sauvage: "Sauvage",
    g12c: "G12C",
    g12d: "G12D",
    g12v: "G12V",
    autre_mute: "Autre mutation",
    non_teste: "Non testé",
  },
  statutMsiDmmr: {
    msi_h: "MSI-H",
    mss: "MSS (non DMMR)",
    dmmr: "DMMR",
    non_teste: "Non testé",
  },
  fusion: { positif: "Positif", negatif: "Négatif", non_teste: "Non testé" },
  resecabilite: {
    resecable: "Résidentielle",
    borderline: "Limite",
    localement_avance: "Localement avancé",
    metastatique: "Métastatique",
    inconnu: "Indéterminée",
  },
  statutDossier: { ouvert: "Ouvert", clos: "Clos", archive: "Archivé" },
};

const NON_RENSEIGNE = "Non renseigné";

function labelEnum(group: string, value: string | null | undefined): string {
  if (value === null || value === undefined || value === "")
    return NON_RENSEIGNE;
  return ENUM_LABELS[group]?.[value] ?? value;
}

function labelTexte(value: string | null | undefined): string {
  if (value === null || value === undefined || value === "")
    return NON_RENSEIGNE;
  return value;
}

// `null` signifie « non renseigné » : l'afficher « Non » serait cliniquement trompeur.
function labelBooleen(value: boolean | null | undefined): string {
  if (value === null || value === undefined) return NON_RENSEIGNE;
  return value ? "Oui" : "Non";
}

function mapDetailToPatient(detail: PatientDetail): PatientData {
  return {
    id: String(detail.id_patient),
    nom: detail.nom,
    prenom: detail.prenom,
    telephone: detail.telephone ?? "",
    adresse: detail.adresse ?? "",
    dateNaissance: formatDateNaissance(detail.date_naissance),
    sexe: detail.sexe === "F" ? "F" : "M",
    age: detail.age ?? computeAge(detail.date_naissance ?? ""),

    ecog: detail.ecog ?? undefined,
    etatNutritionnel: labelEnum("etatNutritionnel", detail.etat_nutritionnel),
    comorbiditesLourdes: detail.comorbidites_lourdes,
    comorbidites: detail.comorbidites,
    douleur:
      detail.douleur_presente === null
        ? undefined
        : detail.douleur_presente
          ? "présente"
          : "absente",
    intensiteDouleur: detail.intensite_douleur ?? undefined,
    ictere: detail.ictere ?? undefined,
    angiocholite: detail.angiocholite ?? undefined,
    diabete: labelEnum("diabete", detail.diabete),
    cholestase: detail.cholestase ?? undefined,

    ca199: detail.ca19_9 ?? undefined,
    ca199MultipleLsn: detail.ca19_9_multiple_lsn ?? undefined,
    bilirubine: detail.bilirubine ?? undefined,
    bilirubineRatioLsn: detail.bilirubine_ratio_lsn ?? undefined,
    statutDpd: labelEnum("statutDpd", detail.statut_dpd),
    albuminemie: detail.albuminemie ?? undefined,

    localisationTumorale: labelEnum(
      "localisationTumorale",
      detail.localisation_tumorale,
    ),
    tailleTumorale: detail.taille_tumorale_cm ?? undefined,
    contactAms: labelEnum("contact", detail.contact_ams),
    contactTroncCoeliaque: labelEnum("contact", detail.contact_tronc_coeliaque),
    contactAhc: labelEnum("contactAhc", detail.contact_art_hepatique),
    contactVmsVp: labelEnum("contactVmsVp", detail.contact_vms_vp),
    adenopathieRegionale: detail.extension_ganglionnaire_regionale ?? undefined,
    adenopathieDistance: detail.extension_ganglionnaire_distance ?? undefined,
    metastases: detail.metastases_presentes ?? undefined,
    siteMetastases: detail.sites_metastases,

    categorieT: detail.categorie_t ?? undefined,
    categorieN: detail.categorie_n ?? undefined,
    categorieM: detail.categorie_m ?? undefined,
    stadeGlobal: detail.stade_global ?? undefined,
    resecabilite: detail.resecabilite ?? undefined,

    preuveHistologique: detail.preuve_histologique ?? undefined,
    statutBrca: labelEnum("statutBrca", detail.statut_brca_germinal),
    statutKras: labelEnum("statutKras", detail.statut_kras),
    statutMsiDmmr: labelEnum("statutMsiDmmr", detail.statut_msi_dmmr),
    fusionNtrk: labelEnum("fusion", detail.fusion_ntrk),
    fusionNrg1: labelEnum("fusion", detail.fusion_nrg1),

    ligneTraitementActuelle: detail.ligne_traitement_actuelle ?? undefined,
    reponseTraitementEnCours: labelTexte(detail.reponse_traitement_en_cours),
    traitementsRecus: detail.traitements_recus,
    traitementsRecusTexte: detail.traitements_recus_texte ?? undefined,
    lignePrecedente: detail.ligne_precedente ?? undefined,
    dureeChimiotherapieMois: detail.duree_chimiotherapie_mois ?? undefined,
    tumeurControle: detail.tumeur_controlee ?? undefined,
    nouvellesMetastases: detail.nouvelles_metastases ?? undefined,
    chirurgieDembleePrevue: detail.chirurgie_d_emblee ?? undefined,
    traitementMedicalPrevu: detail.traitement_medical_prevu ?? undefined,
    pasDeProgressionApres16SemainesPlatine:
      detail.pas_de_progression_apres_16_semaines_platine ?? undefined,
    toxiciteResiduelle: detail.toxicite_residuelle ?? undefined,
    detailsToxicite: detail.details_toxicite ?? undefined,
  };
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<PatientData[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedPatient, setSelectedPatient] = useState<PatientData | null>(
    null,
  );
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<
    "demo" | "clinique" | "bio" | "imagerie" | "tnm" | "histo" | "parcours"
  >("demo");
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);

  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setLoadError(null);
    getPatients()
      .then((list) => {
        if (!active) return;
        setPatients(
          list.map((p) => ({
            id: String(p.id_patient),
            nom: p.nom,
            prenom: p.prenom,
            telephone: p.telephone ?? "",
            adresse: p.adresse ?? "",
            dateNaissance: formatDateNaissance(p.date_naissance),
            sexe: p.sexe === "F" ? "F" : "M",
            age: computeAge(p.date_naissance ?? ""),
            categorieT: p.categorie_t ?? undefined,
            categorieN: p.categorie_n ?? undefined,
            categorieM: p.categorie_m ?? undefined,
          })),
        );
      })
      .catch((cause: unknown) => {
        if (!active) return;
        const detail =
          typeof cause === "object" && cause !== null && "detail" in cause
            ? String((cause as { detail: unknown }).detail)
            : "Impossible de charger la liste des patients.";
        setLoadError(detail);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  // Ferme le menu contextuel si on clique à l'extérieur
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpenMenuId(null);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredPatients = patients.filter(
    (p) =>
      `${p.nom} ${p.prenom}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.telephone.includes(searchTerm) ||
      p.id.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  // Ouvre la modale immédiatement (données de la liste), puis la complète avec
  // la fiche détaillée du patient pour les onglets cliniques.
  const handleOpenDetail = async (patient: PatientData) => {
    setSelectedPatient(patient);
    setActiveTab("demo");
    setDetailError(null);
    setDetailLoading(true);
    try {
      const detail = await getPatientDetail(patient.id);
      setSelectedPatient((current) =>
        current?.id === patient.id ? mapDetailToPatient(detail) : current,
      );
    } catch (cause) {
      const message =
        typeof cause === "object" && cause !== null && "detail" in cause
          ? String((cause as { detail: unknown }).detail)
          : cause instanceof Error
            ? cause.message
            : "Impossible de charger la fiche détaillée du patient.";
      setDetailError(message);
    } finally {
      setDetailLoading(false);
    }
  };

  const handleCloseDetail = () => {
    setSelectedPatient(null);
    setDetailError(null);
    setDetailLoading(false);
  };

  return (
    <div className="space-y-6 font-serif">
      {/* EN-TÊTE & BOUTON AJOUTER PATIENT */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-[#1F3D4D]">Mes Patients</h1>
          <p className="text-xs text-gray-500 mt-1">
            Gestion et consultation des fiches médicales complètes.
          </p>
        </div>

        <Link
          href="/dashboard/patients/add"
          className="px-5 py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl shadow-md transition-all flex items-center gap-2 shrink-0"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
          Nouveau Patient
        </Link>
      </div>

      {/* RECHERCHE */}
      <div className="relative">
        <input
          type="text"
          placeholder="Rechercher par nom, prénom, ID ou téléphone..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-11 pr-4 py-3 bg-white rounded-xl border border-gray-200 text-xs text-[#1F3D4D] focus:outline-none focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 shadow-sm"
        />
        <svg
          className="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {/* LISTE DES PATIENTS */}
      {loading ? (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-10 text-center text-sm text-gray-500">
          Chargement des patients…
        </div>
      ) : loadError ? (
        <div className="bg-red-50 rounded-2xl border border-red-200 p-6 text-center">
          <p className="text-sm font-semibold text-red-700 mb-2">
            Erreur de chargement
          </p>
          <p className="text-xs text-red-600 mb-4">{loadError}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-[#1D7893] hover:bg-[#209BBF] text-white text-xs font-semibold rounded-xl transition"
          >
            Réessayer
          </button>
        </div>
      ) : filteredPatients.length === 0 ? (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-10 text-center">
          <p className="text-sm font-semibold text-[#1F3D4D] mb-1">
            Aucun patient trouvé
          </p>
          <p className="text-xs text-gray-500">
            {patients.length === 0
              ? "Aucun patient enregistré. Créez un premier dossier via « Nouveau Patient »."
              : "Aucun résultat pour cette recherche."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredPatients.map((patient) => (
            <div
              key={patient.id}
              className="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between relative"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-[#209BBF] bg-cyan-50 px-2.5 py-1 rounded-md">
                      {patient.id}
                    </span>
                    <span className="text-xs font-semibold text-gray-500 bg-gray-50 px-2 py-1 rounded-lg">
                      {patient.age} ans ({patient.sexe})
                    </span>
                  </div>

                  {/* MENU À 3 POINTS (Contextual Menu) */}
                  <div className="relative">
                    <button
                      onClick={() =>
                        setOpenMenuId(
                          openMenuId === patient.id ? null : patient.id,
                        )
                      }
                      className="p-1.5 text-gray-400 hover:text-[#1F3D4D] hover:bg-gray-100 rounded-lg transition-colors"
                      aria-label="Actions"
                    >
                      <svg
                        className="w-5 h-5"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
                      </svg>
                    </button>

                    {/* POPUP MENU */}
                    {openMenuId === patient.id && (
                      <div
                        ref={menuRef}
                        className="absolute right-0 mt-1 w-48 bg-white border border-gray-100 rounded-xl shadow-lg z-20 py-1 text-xs text-gray-700 animate-in fade-in zoom-in-95 duration-100"
                      >
                        <Link
                          href={`/dashboard/patients/${patient.id}/edit`}
                          className="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 text-gray-700 font-medium transition"
                          onClick={() => setOpenMenuId(null)}
                        >
                          <svg
                            className="w-4 h-4 text-gray-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth="2"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                            />
                          </svg>
                          Update Patient
                        </Link>
                      </div>
                    )}
                  </div>
                </div>

                <h3 className="text-base font-bold text-[#1F3D4D]">
                  {patient.nom.toUpperCase()} {patient.prenom}
                </h3>
                <div className="mt-3 space-y-1.5 text-xs text-gray-600 border-t border-gray-50 pt-3">
                  <p>
                    <span className="text-gray-400">Tél:</span>{" "}
                    {patient.telephone}
                  </p>
                  <p>
                    <span className="text-gray-400">Stade TNM:</span>{" "}
                    {patient.categorieT || "—"}
                    {patient.categorieN || ""}
                    {patient.categorieM || ""}
                  </p>
                </div>
              </div>

              {/* BOUTONS D'ACTION (Voir Détails & Évaluations) */}
              <div className="mt-4 flex flex-col sm:flex-row gap-2">
                <button
                  onClick={() => handleOpenDetail(patient)}
                  className="flex-1 py-2 bg-[#EAF4F7] hover:bg-[#1D7893] text-[#1D7893] hover:text-white rounded-xl text-xs font-semibold transition text-center"
                >
                  Voir Détails
                </button>

                <Link
                  href={`/dashboard/patients/${patient.id}/evaluations`}
                  className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-xs font-medium text-gray-700 rounded-xl transition text-center"
                >
                  Toutes Évaluations
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* MODAL COMPLÈTE */}
      <AnimatePresence>
        {selectedPatient && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] flex flex-col"
            >
              {/* EN-TÊTE MODALE */}
              <div className="flex items-center justify-between border-b border-gray-100 pb-4">
                <div>
                  <span className="text-xs font-bold text-[#209BBF] bg-cyan-50 px-2.5 py-1 rounded-md">
                    {selectedPatient.id}
                  </span>
                  <h2 className="text-xl font-bold text-[#1F3D4D] mt-1">
                    {selectedPatient.nom.toUpperCase()} {selectedPatient.prenom}
                  </h2>
                </div>
                <button
                  onClick={handleCloseDetail}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-full bg-gray-50"
                >
                  ✕
                </button>
              </div>

              {detailError && (
                <div className="mt-3 bg-amber-50 border border-amber-200 text-amber-800 text-xs rounded-xl px-3 py-2">
                  Fiche clinique indisponible ({detailError}). Les
                  donnéesAffichées se limitent à l&apos;identité du patient.
                </div>
              )}

              {/* NAVIGATION ONGLETS */}
              <div className="flex gap-2 border-b border-gray-100 my-4 overflow-x-auto text-xs pb-2">
                {[
                  { id: "demo", label: "Démographie" },
                  { id: "clinique", label: "Clinique" },
                  { id: "bio", label: "Biologie" },
                  { id: "imagerie", label: "Imagerie" },
                  { id: "tnm", label: "TNM" },
                  { id: "histo", label: "Histologie" },
                  { id: "parcours", label: "Parcours" },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`px-3 py-1.5 rounded-lg font-semibold whitespace-nowrap transition ${
                      activeTab === tab.id
                        ? "bg-[#1D7893] text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* CONTENU SELON L'ONGLET ACTIF */}
              <div className="flex-1 overflow-y-auto space-y-3 text-xs text-gray-700 pr-1">
                {detailLoading && (
                  <div className="flex items-center justify-center gap-2 py-2 text-gray-500">
                    <svg
                      className="w-4 h-4 animate-spin text-[#209BBF]"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      />
                    </svg>
                    <span>Chargement de la fiche clinique…</span>
                  </div>
                )}

                {activeTab === "demo" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div>
                      <span className="text-gray-400 block">Sexe</span>
                      <b>{selectedPatient.sexe}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Âge</span>
                      <b>{selectedPatient.age} ans</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Date de Naissance
                      </span>
                      <b>{labelTexte(selectedPatient.dateNaissance)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Téléphone</span>
                      <b>{labelTexte(selectedPatient.telephone)}</b>
                    </div>
                    <div className="col-span-2">
                      <span className="text-gray-400 block">Adresse</span>
                      <b>{labelTexte(selectedPatient.adresse)}</b>
                    </div>
                  </div>
                )}

                {activeTab === "clinique" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div>
                      <span className="text-gray-400 block">ECOG / PS</span>
                      <b>
                        {selectedPatient.ecog !== undefined
                          ? selectedPatient.ecog
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        État Nutritionnel
                      </span>
                      <b>
                        {labelEnum(
                          "etatNutritionnel",
                          selectedPatient.etatNutritionnel,
                        )}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Comorbidités lourdes
                      </span>
                      <b>{labelBooleen(selectedPatient.comorbiditesLourdes)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Douleur</span>
                      <b>
                        {selectedPatient.douleur === undefined
                          ? NON_RENSEIGNE
                          : selectedPatient.douleur === "présente"
                            ? `Présente${selectedPatient.intensiteDouleur !== undefined ? ` (intensité ${selectedPatient.intensiteDouleur}/10)` : ""}`
                            : "Absente"}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Ictère</span>
                      <b>{labelBooleen(selectedPatient.ictere)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Angiocholite</span>
                      <b>{labelBooleen(selectedPatient.angiocholite)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Diabète</span>
                      <b>{labelEnum("diabete", selectedPatient.diabete)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Cholestase</span>
                      <b>{labelBooleen(selectedPatient.cholestase)}</b>
                    </div>
                    <div className="col-span-2">
                      <span className="text-gray-400 block">
                        Comorbidités déclarées
                      </span>
                      <b>
                        {selectedPatient.comorbidites &&
                        selectedPatient.comorbidites.length > 0
                          ? selectedPatient.comorbidites.join(", ")
                          : "Aucune"}
                      </b>
                    </div>
                  </div>
                )}

                {activeTab === "bio" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div>
                      <span className="text-gray-400 block">CA 19-9</span>
                      <b>
                        {selectedPatient.ca199 !== undefined
                          ? `${selectedPatient.ca199} U/mL`
                          : NON_RENSEIGNE}
                      </b>
                      {selectedPatient.ca199 !== undefined &&
                        selectedPatient.ca199 > 500 && (
                          <span className="ml-2 text-[10px] text-red-500 font-bold">
                            ({">"}500)
                          </span>
                        )}
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        CA 19-9 (x LSN)
                      </span>
                      <b>
                        {selectedPatient.ca199MultipleLsn !== undefined
                          ? `${selectedPatient.ca199MultipleLsn}× LSN`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Bilirubine totale
                      </span>
                      <b>
                        {selectedPatient.bilirubine !== undefined
                          ? `${selectedPatient.bilirubine} µmol/L`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Ratio bilirubine / LSN
                      </span>
                      <b>
                        {selectedPatient.bilirubineRatioLsn !== undefined
                          ? `${selectedPatient.bilirubineRatioLsn.toFixed(2)}× LSN`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Statut DPD</span>
                      <b
                        className={
                          selectedPatient.statutDpd &&
                          selectedPatient.statutDpd !== "Normal" &&
                          selectedPatient.statutDpd !== "Non testé"
                            ? "text-amber-600"
                            : ""
                        }
                      >
                        {labelEnum("statutDpd", selectedPatient.statutDpd)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Albuminémie</span>
                      <b>
                        {selectedPatient.albuminemie !== undefined
                          ? `${selectedPatient.albuminemie} g/L`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                  </div>
                )}

                {activeTab === "imagerie" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div>
                      <span className="text-gray-400 block">Localisation</span>
                      <b>
                        {labelEnum(
                          "localisationTumorale",
                          selectedPatient.localisationTumorale,
                        )}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Taille tumorale
                      </span>
                      <b>
                        {selectedPatient.tailleTumorale !== undefined
                          ? `${selectedPatient.tailleTumorale} cm`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Contact AMS</span>
                      <b>{labelEnum("contact", selectedPatient.contactAms)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Contact Tronc Cœliaque
                      </span>
                      <b>
                        {labelEnum(
                          "contact",
                          selectedPatient.contactTroncCoeliaque,
                        )}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Contact AHC</span>
                      <b>
                        {labelEnum("contactAhc", selectedPatient.contactAhc)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Contact VMS / VP
                      </span>
                      <b>
                        {labelEnum(
                          "contactVmsVp",
                          selectedPatient.contactVmsVp,
                        )}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Adénopathie régionale
                      </span>
                      <b>
                        {labelBooleen(selectedPatient.adenopathieRegionale)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Adénopathie à distance
                      </span>
                      <b>{labelBooleen(selectedPatient.adenopathieDistance)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Métastases</span>
                      <b
                        className={
                          selectedPatient.metastases ? "text-red-600" : ""
                        }
                      >
                        {labelBooleen(selectedPatient.metastases)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Site(s) métastatique(s)
                      </span>
                      <b>
                        {selectedPatient.siteMetastases &&
                        selectedPatient.siteMetastases.length > 0
                          ? selectedPatient.siteMetastases.join(", ")
                          : selectedPatient.metastases === false
                            ? "Aucun"
                            : NON_RENSEIGNE}
                      </b>
                    </div>
                  </div>
                )}

                {activeTab === "tnm" && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4 bg-gray-50 p-4 rounded-xl text-center">
                      <div>
                        <span className="text-gray-400 block">T</span>
                        <b className="text-base text-[#1D7893]">
                          {selectedPatient.categorieT ?? "—"}
                        </b>
                      </div>
                      <div>
                        <span className="text-gray-400 block">N</span>
                        <b className="text-base text-[#1D7893]">
                          {selectedPatient.categorieN ?? "—"}
                        </b>
                      </div>
                      <div>
                        <span className="text-gray-400 block">M</span>
                        <b className="text-base text-[#1D7893]">
                          {selectedPatient.categorieM ?? "—"}
                        </b>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                      <div>
                        <span className="text-gray-400 block">
                          Stade global
                        </span>
                        <b>{labelTexte(selectedPatient.stadeGlobal)}</b>
                      </div>
                      <div>
                        <span className="text-gray-400 block">
                          Résécabilité
                        </span>
                        <b>
                          {labelEnum(
                            "resecabilite",
                            selectedPatient.resecabilite,
                          )}
                        </b>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === "histo" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div className="col-span-2 pb-2 border-b border-gray-200/60">
                      <span className="text-gray-400 block">
                        Preuve Histologique obtenue
                      </span>
                      <b
                        className={
                          selectedPatient.preuveHistologique === undefined
                            ? "text-gray-500"
                            : selectedPatient.preuveHistologique
                              ? "text-emerald-700 font-bold"
                              : "text-amber-700 font-bold"
                        }
                      >
                        {selectedPatient.preuveHistologique === undefined
                          ? NON_RENSEIGNE
                          : selectedPatient.preuveHistologique
                            ? "Oui — Preuve disponible"
                            : "Non — Absente"}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Statut BRCA</span>
                      <b>
                        {labelEnum("statutBrca", selectedPatient.statutBrca)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Statut KRAS</span>
                      <b>
                        {labelEnum("statutKras", selectedPatient.statutKras)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Statut MSI / dMMR
                      </span>
                      <b>
                        {labelEnum(
                          "statutMsiDmmr",
                          selectedPatient.statutMsiDmmr,
                        )}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">Fusion NTRK</span>
                      <b>{labelEnum("fusion", selectedPatient.fusionNtrk)}</b>
                    </div>
                    <div className="col-span-2">
                      <span className="text-gray-400 block">Fusion NRG1</span>
                      <b>{labelEnum("fusion", selectedPatient.fusionNrg1)}</b>
                    </div>
                  </div>
                )}

                {/* PARCOURS THÉRAPEUTIQUE DÉTAILLÉ */}
                {activeTab === "parcours" && (
                  <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
                    <div>
                      <span className="text-gray-400 block">
                        Ligne de traitement actuelle
                      </span>
                      <b>
                        {selectedPatient.ligneTraitementActuelle !== undefined
                          ? `${selectedPatient.ligneTraitementActuelle}e ligne`
                          : NON_RENSEIGNE}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Réponse au traitement en cours
                      </span>
                      <b>
                        {labelTexte(selectedPatient.reponseTraitementEnCours)}
                      </b>
                    </div>

                    <div className="col-span-2 pb-2 border-b border-gray-200/60">
                      <span className="text-gray-400 block">
                        Traitements déjà reçus
                      </span>
                      <b>
                        {selectedPatient.traitementsRecus &&
                        selectedPatient.traitementsRecus.length > 0
                          ? selectedPatient.traitementsRecus.join(" → ")
                          : selectedPatient.traitementsRecusTexte
                            ? selectedPatient.traitementsRecusTexte
                            : "Aucun"}
                      </b>
                    </div>

                    <div>
                      <span className="text-gray-400 block">
                        Ligne précédente (déduite)
                      </span>
                      <b>{labelTexte(selectedPatient.lignePrecedente)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Durée chimiothérapie (mois)
                      </span>
                      <b>
                        {selectedPatient.dureeChimiotherapieMois !== undefined
                          ? `${selectedPatient.dureeChimiotherapieMois} mois`
                          : NON_RENSEIGNE}
                      </b>
                    </div>

                    <div>
                      <span className="text-gray-400 block">
                        Tumeur contrôlée
                      </span>
                      <b>{labelBooleen(selectedPatient.tumeurControle)}</b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Nouvelles métastases
                      </span>
                      <b
                        className={
                          selectedPatient.nouvellesMetastases
                            ? "text-red-600"
                            : ""
                        }
                      >
                        {labelBooleen(selectedPatient.nouvellesMetastases)}
                      </b>
                    </div>

                    <div>
                      <span className="text-gray-400 block">
                        Chirurgie d&apos;emblée prévue
                      </span>
                      <b>
                        {labelBooleen(selectedPatient.chirurgieDembleePrevue)}
                      </b>
                    </div>
                    <div>
                      <span className="text-gray-400 block">
                        Traitement médical prévu
                      </span>
                      <b>
                        {labelBooleen(selectedPatient.traitementMedicalPrevu)}
                      </b>
                    </div>

                    <div className="col-span-2">
                      <span className="text-gray-400 block">
                        Pas de progression après 16 sem. de platine
                      </span>
                      <b>
                        {labelBooleen(
                          selectedPatient.pasDeProgressionApres16SemainesPlatine,
                        )}
                      </b>
                    </div>

                    <div className="col-span-2 pt-2 border-t border-gray-200/60">
                      <span className="text-gray-400 block">
                        Toxicité résiduelle
                      </span>
                      <b>
                        {selectedPatient.toxiciteResiduelle === true
                          ? `Oui${selectedPatient.detailsToxicite ? ` (${selectedPatient.detailsToxicite})` : ""}`
                          : labelBooleen(selectedPatient.toxiciteResiduelle)}
                      </b>
                    </div>
                  </div>
                )}
              </div>

              {/* PIED DE MODALE */}
              <div className="mt-6 pt-4 border-t border-gray-100 flex items-center justify-between gap-2">
                <Link
                  href={`/dashboard/patients/${selectedPatient.id}/edit`}
                  onClick={handleCloseDetail}
                  className="px-4 py-2.5 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-xl text-xs font-semibold transition"
                >
                  Update Patient
                </Link>
                <button
                  onClick={handleCloseDetail}
                  className="px-6 py-2.5 bg-[#1D7893] text-white rounded-xl text-xs font-semibold hover:bg-[#209BBF] transition"
                >
                  Fermer
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
