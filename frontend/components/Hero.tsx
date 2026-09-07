import Image from "next/image";
import Link from "next/link";
import heroImg from "@/assets/hero-doctors.png"; // Ajuste le chemin si placé dans public/

export default function Hero() {
  return (
    <section className="relative w-full h-[550px] md:h-[700px] overflow-hidden bg-gray-900">
      
      {/* 1. IMAGE DE FOND (MÉDECINS) */}
      <div className="absolute inset-0 w-full h-full">
        <Image
          src={heroImg}
          alt="Équipe médicale PancreaCare"
          fill
          priority
          className="object-cover object-center"
        />
      </div>

      {/* 2. BLOC BLEU AVEC COUPE DIAGONALE (OVERLAY) */}
      <div 
        className="absolute inset-y-0 left-0 w-full md:w-[60%] bg-[#1D7893]/90 flex flex-col justify-center px-8 sm:px-12 md:px-20 text-white z-10"
        style={{ clipPath: "polygon(0 0, 100% 0, 85% 100%, 0% 100%)" }}
      >
        <div className="max-w-xl space-y-6">
          
          {/* Titre principal */}
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold leading-tight tracking-tight">
            L'expertise médicale, la transparence en plus
          </h1>

          {/* Sous-titre */}
          <p className="text-sm sm:text-base md:text-lg text-cyan-50 font-light max-w-lg leading-relaxed">
            Un système d'aide à la décision médicale basé sur les guides cliniques pour le diagnostic et le suivi du cancer du pancréas.
          </p>

          {/* Bouton d'action */}
          <div className="pt-2">
            <Link
              href="login?mode=signup"
              className="inline-block px-8 py-3.5 bg-[#0F4C5C] hover:bg-[#0b3844] text-white font-medium text-sm rounded-lg shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"
            >
              Commencer
            </Link>
          </div>

        </div>
      </div>

    </section>
  );
}