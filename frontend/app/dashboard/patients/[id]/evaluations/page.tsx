"use client";

import { use } from "react";
import Link from "next/link";

interface Evaluation {
  id: string;
  number: string; // Ex: "Évaluation 01"
  date: string;
  doctor: string;
}

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function PatientEvaluationsPage({ params }: PageProps) {
  const { id } = use(params);

  // Exemple de données (à remplacer par votre appel API ou state)
  const evaluations: Evaluation[] = [
    {
      id: "eval-001",
      number: "Évaluation 01",
      date: "12 Janvier 2026",
      doctor: "Dr. Sofiane Benali",
    
    },
    {
      id: "eval-002",
      number: "Évaluation 02",
      date: "05 Février 2026",
      doctor: "Dr. Sofiane Benali",
      
    },
    {
      id: "eval-003",
      number: "Évaluation 03",
      date: "28 Février 2026",
      doctor: "Dr. Sofiane Benali",
      
    },
  ];

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
          className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          ← Retour aux Patients
        </Link>
      </div>

      {/* Grille des cartes Évaluations */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {evaluations.map((item) => (
          <Link
            key={item.id}
            href={`/dashboard/evaluation?patientId=${id}&evalId=${item.id}`}
            className="group relative bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#209BBF]/40 transition duration-200 flex flex-col justify-between"
          >
            <div>
              {/* Badge Statut + Icone */}
              <div className="flex items-center justify-between mb-4">
               
              </div>

              {/* Titre & Date */}
              <h3 className="text-lg font-bold text-[#1F3D4D] group-hover:text-[#209BBF] transition">
                {item.number}
              </h3>
              <p className="text-xs text-gray-400 mt-1">
                Enregistrée le : <span className="font-medium text-gray-600">{item.date}</span>
              </p>
              <p className="text-xs text-gray-400 mt-0.5">
                Par : <span className="font-medium text-gray-600">{item.doctor}</span>
              </p>
            </div>

            {/* Pied de la carte */}
            <div className="mt-6 pt-3 border-t border-gray-50 flex items-center justify-between text-xs text-[#209BBF] font-semibold">
              <span>Ouvrir l'évaluation</span>
              <span className="transform group-hover:translate-x-1 transition">→</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}