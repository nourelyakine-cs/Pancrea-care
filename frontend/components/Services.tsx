import Image from "next/image";
import service1Img from "@/assets/service-pancreas.png"; 
import service2Img from "@/assets/folder.jpg"; 
import service3Img from "@/assets/service-tncd.png"; 
// 1. IMPORTATIVE DE VOTRE IMAGE D'ARRIÈRE-PLAN (ajustez le chemin et le nom du fichier)
import bgServices from "@/assets/bg-services.png"; 

export default function Services() {
  return (
    <section id="nos-services" className="w-full py-25 px-6 sm:px-12 md:px-20 relative overflow-hidden">
      
      {/* 2. IMAGE D'ARRIÈRE-PLAN CUSTOMISÉE */}
      <div className="absolute inset-0 w-full h-full z-0">
        <Image 
          src={bgServices} 
          alt="Arrière-plan Nos Services" 
          fill
          priority
          className="object-cover object-center opacity-60" // Ajustez opacity-20 (ex: opacity-10 ou opacity-30) selon la lisibilité
        />
        {/* Optionnel : un léger filtre coloré par-dessus pour harmoniser */}
        
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        
        {/* TITRE DE LA SECTION */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#1D7893] tracking-tight">
            Nos Services
          </h2>
          <div className="w-24 h-1 bg-[#209BBF] mx-auto mt-4 rounded-full"></div>
        </div>

        {/* GRILLE DES 3 CARTES AVEC BORDURES ET OMBRES */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          
          {/* CARTE 1 */}
          <div className="group bg-white/90 backdrop-blur-sm rounded-3xl p-6 flex flex-col justify-between shadow-md hover:shadow-2xl border border-gray-100 hover:border-[#209BBF]/40 transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-center pt-2 mb-6">
              <h3 className="text-xl sm:text-2xl font-bold text-[#1F3D4D] group-hover:text-[#209BBF] transition-colors duration-300 leading-snug">
                Recommandations Cancer du Pancréas
              </h3>
            </div>
            
            <div className="relative w-full h-48 rounded-2xl overflow-hidden border border-gray-100 mt-auto">
              <Image 
                src={service1Img} 
                alt="Recommandations Cancer du Pancréas" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>
          </div>

          {/* CARTE 2 */}
          <div className="group bg-white/90 backdrop-blur-sm rounded-3xl p-6 flex flex-col justify-between shadow-md hover:shadow-2xl border border-gray-100 hover:border-[#209BBF]/40 transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-center pt-2 mb-6">
              <h3 className="text-xl sm:text-2xl font-bold text-[#1F3D4D] group-hover:text-[#209BBF] transition-colors duration-300 leading-snug">
                Historique & Suivi Patients
              </h3>
            </div>
            
            <div className="relative w-full h-48 rounded-2xl overflow-hidden border border-gray-100 mt-auto">
              <Image 
                src={service2Img} 
                alt="Historique et suivi" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>
          </div>

          {/* CARTE 3 */}
          <div className="group bg-white/90 backdrop-blur-sm rounded-3xl p-6 flex flex-col justify-between shadow-md hover:shadow-2xl border border-gray-100 hover:border-[#209BBF]/40 transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-center pt-2 mb-6">
              <h3 className="text-xl sm:text-2xl font-bold text-[#1F3D4D] group-hover:text-[#209BBF] transition-colors duration-300 leading-snug">
                Support à la Décision Médicale selon TNCD
              </h3>
            </div>
            
            <div className="relative w-full h-48 rounded-2xl overflow-hidden border border-gray-100 mt-auto">
              <Image 
                src={service3Img} 
                alt="Support à la décision selon TNCD" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}