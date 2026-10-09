import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PancreaCare",
  description: "Système expert déterministe pour la prise en charge médicale",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" className="h-full antialiased scroll-smooth">
      <body className="min-h-full flex flex-col font-serif">
        {children}
      </body>
    </html>
  );
}