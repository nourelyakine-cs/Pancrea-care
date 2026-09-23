"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Loader2, CalendarClock, Stethoscope, Activity, FileQuestion } from "lucide-react";
import { getPatientEvaluations, type EvaluationResume } from "@/lib/api";

interface PageProps {
  params: Promise<{ id: string }>;
}

const CONTEXTE_LABEL: Record<string, string> = {
  diagnostic: "Diagnostic initial",
  pre_neoadjuvant: "Pré-néoadjuvant",
  restaging: "Restaging",
  pre_chirurgie: "Pré-chirurgie",
  adjuvant: "Adjuvant",
  surveillance: "Surveillance",
  recidive: "Récidive",
};

const RESECABILITE_META: Record<string, { label: string; className: string }> = {
  resecable: { label: "Résécable", className: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  borderline: { label: "Borderline", className: "bg-amber-50 text-amber-700 border-amber-200" },
  localement_avance: { label: "Localement avancé", className: "bg-orange-50 text-orange-700 border-orange-200" },
  metastatique: { label: "Métastatique", className: "bg-red-50 text-red-700 border-red-200" },
  inconnu: { label: "Non déterminée", className: "bg-gray-50 text-gray-600 border-gray-200" },
};

const formatDate = (iso: string | null | undefined) =>
  iso ? new Date(iso).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }) : "—";

export default function PatientEvaluationsPage({ params }: PageProps) {
  const { id } = use(params);

  const [evaluations, setEvaluations] = useState<EvaluationResume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    getPatientEvaluations(id)
      .then((data) => {
        if (active) setEvaluations(data);
      })
      .catch((cause) => {
        if (active) setError(cause instanceof Error ? cause.message : "Impossible de charger les évaluations.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [id]);

  return (
    <div className="max-w-6xl mx-auto space-y-6 p-6 font-serif">
      {/* En-tête de la page */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between bg-white p-6 rounded-2xl border border-gray-100 shadow-sm gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#209BBF] bg-cyan-50 px-2.5 py-1 rounded-md">
              {id}
            </span>
            <span className="text-xs text-gray-400">• Dossier Médical</span>
          </div>
          <h1 className="text-2xl font-bold text-[#1F3D4D] mt-2">
            Historique des Évaluations
          </h1>
          <p className="text-xs text-gray-500 mt-1">
            Consultez ou gérez l'ensemble des fiches d'évaluation du patient.
          </p>
        </div>

        <Link
          href="/dashboard/patients"
          className="inline-flex items-center gap-2 justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          <ArrowLeft className="w-4 h-4" /> Retour aux Patients
        </Link>
      </div>

      {/* États de chargement / erreur / vide */}
      {loading && (
        <div className="flex flex-col items-center justify-center p-12 bg-white rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <Loader2 className="w-8 h-8 animate-spin text-[#1D7893]" />
          <p className="text-sm font-medium text-gray-600">Chargement des évaluations...</p>
        </div>
      )}

      {!loading && error && (
        <div className="p-6 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
          <b>Erreur de chargement :</b> {error}
        </div>
      )}

      {!loading && !error && evaluations.length === 0 && (
        <div className="flex flex-col items-center justify-center p-12 bg-white rounded-2xl border border-gray-100 shadow-sm space-y-3 text-center">
          <FileQuestion className="w-8 h-8 text-gray-300" />
          <p className="text-sm font-medium text-gray-600">
            Aucune évaluation enregistrée pour ce patient.
          </p>
          <p className="text-xs text-gray-400">
            Les évaluations créées depuis la fiche de saisie patient apparaîtront ici.
          </p>
        </div>
      )}

      {/* Grille des cartes Évaluations */}
      {!loading && !error && evaluations.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {evaluations.map((item) => {
            const resecabilite = RESECABILITE_META[item.resecabilite ?? "inconnu"] ?? RESECABILITE_META.inconnu;
            const stadeTnm = `${item.categorie_t ?? ""}${item.categorie_n ?? ""}${item.categorie_m ?? ""}`;
            const medecin = item.medecin_nom
              ? `Dr. ${item.medecin_prenom ?? ""} ${item.medecin_nom}`.trim()
              : "Médecin non renseigné";

            return (
              <Link
                key={item.id_evaluation}
                href={`/dashboard/evaluation?patientId=${id}&evalId=${item.id_evaluation}`}
                className="group relative bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#209BBF]/40 transition duration-200 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-4 gap-2">
                    <span className="text-[10px] font-bold text-[#209BBF] bg-cyan-50 px-2.5 py-1 rounded-md">
                      Évaluation #{String(item.id_evaluation).padStart(3, "0")}
                    </span>
                    <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full border ${resecabilite.className}`}>
                      {resecabilite.label}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-[#1F3D4D] group-hover:text-[#209BBF] transition">
                    {CONTEXTE_LABEL[item.contexte ?? ""] ?? item.contexte ?? "Évaluation clinique"}
                  </h3>

                  <div className="mt-3 space-y-1 text-xs text-gray-500">
                    <p className="flex items-center gap-1.5">
                      <CalendarClock className="w-3.5 h-3.5 text-gray-400" />
                      Enregistrée le : <span className="font-medium text-gray-600">{formatDate(item.date_evaluation)}</span>
                    </p>
                    <p className="flex items-center gap-1.5">
                      <Stethoscope className="w-3.5 h-3.5 text-gray-400" />
                      Par : <span className="font-medium text-gray-600">{medecin}</span>
                    </p>
                    {stadeTnm && (
                      <p className="flex items-center gap-1.5">
                        <Activity className="w-3.5 h-3.5 text-gray-400" />
                        TNM : <span className="font-medium text-gray-600">{stadeTnm}</span>
                        {item.stade_global ? <span className="text-gray-400">· Stade {item.stade_global}</span> : null}
                      </p>
                    )}
                  </div>
                </div>

                <div className="mt-6 pt-3 border-t border-gray-50 flex items-center justify-between text-xs text-[#209BBF] font-semibold">
                  <span>Ouvrir l'évaluation</span>
                  <span className="transform group-hover:translate-x-1 transition">→</span>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}