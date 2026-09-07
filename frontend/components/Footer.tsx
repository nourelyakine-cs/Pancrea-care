import Link from "next/link";
import { Phone, MapPin, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer id="contact" className="w-full bg-[#D4E8ED] text-[#1F3D4D] pt-14 pb-6 px-6 sm:px-12 md:px-20 border-t border-cyan-200/50">
      <div className="max-w-7xl mx-auto">
        
        {/* GRILLE 3 COLONNES CONFORME AU FIGMA */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 items-start mb-12 text-center md:text-left">
          
          {/* COLONNE 1 : LOGO + NAVIGATION */}
          <div className="space-y-4 flex flex-col items-center md:items-start">
            <h3 className="text-2xl font-extrabold text-[#1D7893] tracking-wide uppercase">
              Pancrea<span className="text-[#209BBF]">Care</span>
            </h3>
            
            <nav className="flex flex-col space-y-2 text-sm font-semibold text-[#1F3D4D]">
              <Link href="#accueil" className="hover:text-[#209BBF] hover:translate-x-1 transition-all duration-200 w-fit">
                Accueil
              </Link>
              <Link href="#a-propos" className="hover:text-[#209BBF] hover:translate-x-1 transition-all duration-200 w-fit">
                À propos
              </Link>
              <Link href="#nos-services" className="hover:text-[#209BBF] hover:translate-x-1 transition-all duration-200 w-fit">
                Nos services
              </Link>
              <Link href="#contact" className="hover:text-[#209BBF] hover:translate-x-1 transition-all duration-200 w-fit">
                Contact
              </Link>
            </nav>
          </div>

          {/* COLONNE 2 : DESCRIPTION CENTRALISÉE + BOUTON */}
          <div className="flex flex-col items-center text-center space-y-5">
            <h4 className="text-xl font-bold text-[#1D7893]">
              PancreaCare
            </h4>
            
            <p className="text-sm text-gray-700 leading-relaxed max-w-xs font-medium">
              Un système expert déterministe qui transforme les guides cliniques en recommandations 100% explicables.
            </p>

            {/* BOUTON SE CONNECTER (Interactif & Stylisé) */}
            <Link 
              href="/login" 
              className="inline-block px-6 py-2.5 text-sm font-semibold text-[#1D7893] border-2 border-[#1D7893] rounded-full hover:bg-[#1D7893] hover:text-white transform hover:scale-105 transition-all duration-300 shadow-sm"
            >
              Se Connecter
            </Link>
          </div>

          {/* COLONNE 3 : INFORMATIONS DE CONTACT */}
          <div className="space-y-4 flex flex-col items-center md:items-start">
            <h4 className="text-lg font-bold text-[#1D7893]">
              Contact
            </h4>

            <div className="space-y-3 text-sm font-medium">
              {/* Téléphone 1 */}
              <div className="flex items-center gap-3 group">
                <div className="p-1.5 bg-white/60 rounded-lg text-[#1D7893] group-hover:bg-[#1D7893] group-hover:text-white transition-colors duration-200">
                  <Phone className="w-4 h-4" />
                </div>
                <span>0236 471 204</span>
              </div>

              {/* Téléphone 2 */}
              <div className="flex items-center gap-3 group">
                <div className="p-1.5 bg-white/60 rounded-lg text-[#1D7893] group-hover:bg-[#1D7893] group-hover:text-white transition-colors duration-200">
                  <Phone className="w-4 h-4" />
                </div>
                <span>0747945531</span>
              </div>

              {/* Localisation */}
              <div className="flex items-center gap-3 group">
                <div className="p-1.5 bg-white/60 rounded-lg text-[#1D7893] group-hover:bg-[#1D7893] group-hover:text-white transition-colors duration-200">
                  <MapPin className="w-4 h-4" />
                </div>
                <span>EHS Aïn Taya</span>
              </div>

              {/* Email */}
              <div className="flex items-center gap-3 group">
                <div className="p-1.5 bg-white/60 rounded-lg text-[#1D7893] group-hover:bg-[#1D7893] group-hover:text-white transition-colors duration-200">
                  <Mail className="w-4 h-4" />
                </div>
                <a href="mailto:contact@pancreacare.dz" className="hover:underline">
                  contact@pancreacare.dz
                </a>
              </div>
            </div>
          </div>

        </div>

        {/* MENTIONS DE COPYRIGHT (BAS DE PAGE) */}
        <div className="pt-6 border-t border-cyan-300/40 text-center text-xs text-gray-600 font-medium">
          © 2026 PancreaCare - EHS Aïn Taya . Tous droits réservés.
        </div>

      </div>
    </footer>
  );
}