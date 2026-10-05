"""Applique une migration SQL depuis le backend.

Usage : python -m app.utils.appliquer_migration <fichier.sql>

Les instructions `BEGIN;` / `COMMIT;` du fichier sont respectées telles
quelles : une transaction doit être ouverte et validée par un seul
connexion, sinon le `COMMIT` du fichier stabulerait dans le vide.
"""

import sys
from pathlib import Path

from sqlalchemy import text

from app.database import engine


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage : python -m app.utils.appliquer_migration <fichier.sql>")
        return 1

    chemin = Path(sys.argv[1])
    if not chemin.is_file():
        print(f"Fichier introuvable : {chemin}")
        return 1

    sql = chemin.read_text(encoding="utf-8")
    print(f"Application de {chemin.name} ({len(sql)} caractères)…")

    with engine.connect() as connexion:
        # BEGIN/COMMIT sont dans le fichier : on ouvre une seule connexion pour
        # que tout s'exécute dans cette transaction-là.
        resultat = connexion.execute(text(sql))
        print(f"OK — {resultat.rowcount} ligne(s)touchée(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
