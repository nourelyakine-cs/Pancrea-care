import Image from "next/image";
import Link from "next/link";
import aboutDoctorsImg from "@/assets/about-doctors.png"; 
import partnerLogoImg from "@/assets/partner-logo.png"; 

export default function About() {
  return (
    <section id="a-propos" className="w-full bg-[#EAF4F7] py-12 px-6 sm:px-12 md:px-20 relative overflow-hidden">
      <div className="max-w-7xl mx-auto relative">
        
        {/* LOGO PARTENAIRE (Positionné en Absolu pour ne plus pousser le titre) */}
        <div className="absolute top-0 right-0 z-10 hidden sm:block">
          <div className="bg-white p-2.5 rounded-2xl shadow-sm border border-cyan-100 flex items-center justify-center">
            <Image 
              src={partnerLogoImg} 
              alt="EPH Partner Logo" 
              width={95} 
              height={95} 
              className="object-contain"
            />
          </div>
        </div>

        {/* TITRE PRINCIPAL CENTRÉ (Maintenant bien haut) */}
        <div className="text-center mb-12 pt-15">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#1D7893] tracking-tight">
            À propos de Pancrea Care
          </h2>
          <div className="w-24 h-1 bg-[#209BBF] mx-auto mt-4 rounded-full"></div>
        </div>

        {/* CONTENU PRINCIPAL (2 COLONNES) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* COLONNE GAUCHE : IMAGE */}
          <div className="lg:col-span-6 relative">
            <div className="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-white">
              <Image 
                src={aboutDoctorsImg} 
                alt="Équipe médicale spécialiste du pancréas" 
                className="w-full h-[450px] object-cover hover:scale-105 transition-transform duration-500"
              />
            </div>
          </div>

          {/* COLONNE DROITE : TEXTE + ENGAGEMENTS */}
          <div className="lg:col-span-6 space-y-6">
            <h3 className="text-2xl sm:text-3xl font-bold text-[#1F3D4D] leading-snug">
              Optimisez la Prise en Charge du Cancer du Pancréas
            </h3>

            <p className="text-gray-700 leading-relaxed text-base sm:text-lg">
              Développé dans le cadre d’un projet de recherche en collaboration avec l’EPH Aïn Taya et l'Initiative DIGIMED, <strong className="text-[#1D7893]">PANCRA CARE</strong> est une plateforme d’aide à la décision clinique dédiée à la prise en charge du cancer du pancréas.
            </p>

            {/* LISTE DES AVANTAGES CLÉS */}
            <div className="space-y-5 pt-4">
              
              <div className="flex items-center gap-5 p-5 bg-white rounded-2xl shadow-md border border-cyan-100/50 transform hover:-translate-y-1 hover:scale-[1.02] hover:shadow-xl transition-all duration-300 cursor-pointer">
                <div className="p-3.5 bg-[#209BBF]/15 rounded-xl text-[#209BBF] shrink-0">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-gray-900">Recommandations Thérapeutiques</h4>
                  <p className="text-sm sm:text-base text-gray-600 mt-1">Propose des algorithmes basés sur les guides cliniques officiels.</p>
                </div>
              </div>

              <div className="flex items-center gap-5 p-5 bg-white rounded-2xl shadow-md border border-cyan-100/50 transform hover:-translate-y-1 hover:scale-[1.02] hover:shadow-xl transition-all duration-300 cursor-pointer">
                <div className="p-3.5 bg-[#209BBF]/15 rounded-xl text-[#209BBF] shrink-0">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-gray-900">Décisions Justifiées & Transparente</h4>
                  <p className="text-sm sm:text-base text-gray-600 mt-1">Un système déterministe garantissant une traçabilité totale des choix médicaux.</p>
                </div>
              </div>

            </div>

            {/* BOUTON D'ACTION */}
            <div className="pt-4">
              <Link 
                href="#nos-services" 
                className="inline-block px-8 py-3.5 bg-[#209BBF] hover:bg-[#1D7893] text-white font-medium rounded-xl shadow-md transition-all duration-300"
              >
                En savoir plus
              </Link>
            </div>

          </div>

        </div>

        {/* BLOC STATISTIQUES */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-16 pt-12 border-t border-cyan-200/60 text-center">
          <div className="p-4 bg-white/40 rounded-2xl">
            <p className="text-3xl font-extrabold text-[#1D7893]">100%</p>
            <p className="text-sm font-medium text-gray-600 mt-1">Explicabilité des algorithmes</p>
          </div>
          <div className="p-4 bg-white/40 rounded-2xl">
            <p className="text-3xl font-extrabold text-[#1D7893]">EPH Aïn Taya</p>
            <p className="text-sm font-medium text-gray-600 mt-1">Partenaire hospitalier clinique</p>
          </div>
          <div className="p-4 bg-white/40 rounded-2xl">
            <p className="text-3xl font-extrabold text-[#1D7893]">DIGIMED</p>
            <p className="text-sm font-medium text-gray-600 mt-1">Projet de recherche innovant</p>
          </div>
        </div>

      </div>
    </section>
  );
}