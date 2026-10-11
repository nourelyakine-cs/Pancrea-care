"""Création du schéma à partir des modèles SQLAlchemy.

    python -m app.init_db

Crée dans la base pointée par `DATABASE_URL` les tables déclarées par les
modèles — c'est-à-dire exactement le schéma attendu par le code. Les tables
déjà présentes sont laissées intactes, donc le script peut être réexécuté.

Il ne crée aucune donnée : les référentiels (gènes, comorbidités, protocoles)
restent vides. Le premier compte d'administration est créé par
`python -m app.bootstrap_admin`.
"""

import importlib

from app.database import Base, engine

MODELES = [
    "medecin",
    "patient",
    "audit",
    "dossier",
    "reference",
    "evaluation",
    "traitement",
    "decision",
    "donnees_derivees",
    "compte",
    "parcours_therapeutique",
]


def main() -> int:
    for module in MODELES:
        importlib.import_module(f"app.models.{module}")

    Base.metadata.create_all(bind=engine)

    noms = sorted(Base.metadata.tables)
    print(f"{len(noms)} tables disponibles dans '{engine.url.database}' :")
    for nom in noms:
        print(f"  - {nom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
