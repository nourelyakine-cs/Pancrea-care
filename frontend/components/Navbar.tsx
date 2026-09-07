"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import logoImg from "@/assets/logo.png";

export default function Navbar() {
  const [activeSection, setActiveSection] = useState<string>("accueil");

  useEffect(() => {
    // Liste des IDs des sections à observer
    const sectionIds = ["accueil", "a-propos", "nos-services", "contact"];
    
    const handleScroll = () => {
      const scrollPosition = window.scrollY + 120; // Décalage pour anticiper le header sticky

      for (const id of sectionIds) {
        const element = document.getElementById(id);
        if (element) {
          const top = element.offsetTop;
          const height = element.offsetHeight;

          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(id);
            break;
          }
        }
      }
      
      // Si tout en haut de la page, forcer 'accueil'
      if (window.scrollY < 100) {
        setActiveSection("accueil");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className="w-full bg-[#FBFBFB] border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-15 flex items-center justify-between">
        
        {/* 1. LOGO */}
        <Link href="/" className="flex items-center justify-center py-2">
          <Image 
            src={logoImg} 
            alt="PANCRA CARE Logo" 
            width={500}
            height={300}
            priority
            className="h-10 w-auto object-contain scale-110"
          />
        </Link>

        {/* 2. MENU DE NAVIGATION DYNAMIQUE */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-semibold">
          <Link 
           href="/"  
            className={`transition-colors duration-200 ${
              activeSection === "accueil" 
                ? "text-[#209BBF] font-bold" 
                : "text-gray-800 hover:text-[#209BBF]"
            }`}
          >
            Accueil
          </Link>

          <Link 
            href="#a-propos" 
            className={`transition-colors duration-200 ${
              activeSection === "a-propos" 
                ? "text-[#209BBF] font-bold" 
                : "text-gray-800 hover:text-[#209BBF]"
            }`}
          >
            À propos
          </Link>

          <Link 
            href="#nos-services" 
            className={`transition-colors duration-200 ${
              activeSection === "nos-services" 
                ? "text-[#209BBF] font-bold" 
                : "text-gray-800 hover:text-[#209BBF]"
            }`}
          >
            Nos services
          </Link>

          <Link 
            href="#contact" 
            className={`transition-colors duration-200 ${
              activeSection === "contact" 
                ? "text-[#209BBF] font-bold" 
                : "text-gray-800 hover:text-[#209BBF]"
            }`}
          >
            Contact
          </Link>
        </nav>

        {/* 3. BOUTONS CONNEXION / INSCRIPTION */}
        <div className="flex items-center gap-3 text-xs font-semibold">
          <Link 
            href="/login" 
            className="px-4 py-2 border border-[#89C5D6] text-[#209BBF] rounded hover:bg-cyan-50 transition"
          >
            Se connecter
          </Link>
          <Link 
            href="/login?mode=signup" 
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:border-[#209BBF] hover:text-[#209BBF] transition"
          >
            S'inscrire
          </Link>
        </div>

      </div>
    </header>
  );
}