"""Création du premier compte d'administration.

    python -m app.bootstrap_admin

Les identifiants sont lus dans l'environnement (`SUPER_ADMIN_EMAIL`,
`SUPER_ADMIN_PASSWORD`, `SUPER_ADMIN_NOM`, `SUPER_ADMIN_PRENOM`) ou demandés
de façon interactive. Rien n'est écrit dans un fichier SQL versionné : un mot
de passe en clair dans le dépôt est un secret divulgué.

L'administrateur est **aussi un praticien** : un profil `medecin` est créé et
rattaché dans la même transaction. Il peut donc passer de `/admin` à
`/dashboard` et utiliser l'interface clinique comme n'importe quel médecin,
et les dossiers qu'il crée portent son identité.

Le compte est créé **directement actif**, et c'est la seule exception à la
règle « tout compte passe par la validation » : le super admin valide les
comptes, il ne peut donc pas se valider lui-même — il n'y a personne pour le
faire. La contrainte `ck_compte_role_admin` de la migration l'impose d'ailleurs.

Relancer le script sur un email déjà pris ne modifie rien : c'est un garde-fou,
une réexécution ne doit pas pouvoir réécrire le mot de passe d'un compte en
production par simple oubli d'une variable d'environnement.
"""

import getpass
import os
import sys
from datetime import datetime, timezone

from sqlalchemy import func

from app.database import SessionLocal
from app.models.compte import Compte
from app.models.enums import RoleCompte, StatutCompte
# `medecin` doit être importé même si le script ne le manipule jamais : la
# colonne `compte.id_medecin` est une clé étrangère vers cette table, et
# SQLAlchemy a besoin de la connaître au moment du INSERT. Sans cet import, le
# premier flush lève NoReferencedTableError et la création échoue.
from app.models.medecin import Medecin  # noqa: F401
from app.schemas.auth import describe_password_errors, failed_password_rules
from app.services import securite


def creer_super_admin(
    email: str, mot_de_passe: str, nom: str, prenom: str
) -> tuple[Compte, bool]:
    """Crée le compte s'il n'existe pas. Renvoie `(compte, cree)`.

    Lève une erreur explicite si l'email est déjà pris : réécrire le mot de
    passe d'un compte existant par simple oubli d'une variable d'environnement
    reviendrait à laisser n'importe qui reprendre le compte d'un
    administrateur.

    Un profil `medecin` est créé **et rattaché** dans la foulée. L'administrateur
    est aussi un praticien : sans profil, `get_medecin_for_user` le refuserait
    sur toutes les routes cliniques et l'interface médecin resterait
    inaccessible. Et comme c'est ce `id_medecin` qui estampille les dossiers
    qu'il crée, un administrateur sans profil ne pourrait rien prescrire sous
    son identité.
    """
    db = SessionLocal()
    try:
        normalise = email.strip().lower()
        existant = (
            db.query(Compte).filter(func.lower(Compte.email) == normalise).first()
        )
        if existant is not None:
            raise SystemExit(
                f"Un compte existe déjà pour {normalise}. "
                "Ce script ne modifie pas un compte existant : utilisez le "
                "tableau de bord d'administration, ou changez d'email."
            )

        # Un profil preexistant avec la même adresse est réutilisé plutôt que
        # dupliqué : `medecin.email` est unique.
        medecin = (
            db.query(Medecin).filter(func.lower(Medecin.email) == normalise).first()
        )
        if medecin is None:
            medecin = Medecin(
                nom=nom.strip(),
                prenom=prenom.strip(),
                email=normalise,
                telephone="",
                hopital="PANCRA",
            )
            db.add(medecin)
            db.flush()
        else:
            medecin.nom = nom.strip()
            medecin.prenom = prenom.strip()

        compte = Compte(
            email=normalise,
            mot_de_passe_hash=securite.hacher_mot_de_passe(mot_de_passe),
            role=RoleCompte.super_admin,
            statut=StatutCompte.actif,
            nom=nom.strip(),
            prenom=prenom.strip(),
            hopital="PANCRA",
            id_medecin=medecin.id_medecin,
            date_activation=datetime.now(timezone.utc),
        )
        db.add(compte)
        db.commit()
        db.refresh(compte)
        return compte, True
    finally:
        db.close()


def _demander(mot: str, defaut: str | None = None) -> str:
    suffixe = f" [{defaut}]" if defaut else ""
    while True:
        valeur = input(f"{mot}{suffixe} : ").strip() or (defaut or "")
        if valeur:
            return valeur
        print("Valeur obligatoire.", file=sys.stderr)


def main() -> int:
    email = os.environ.get("SUPER_ADMIN_EMAIL")
    mot_de_passe = os.environ.get("SUPER_ADMIN_PASSWORD")
    nom = os.environ.get("SUPER_ADMIN_NOM")
    prenom = os.environ.get("SUPER_ADMIN_PRENOM")

    if not email:
        email = _demander("Email de l'administrateur")
    if not mot_de_passe:
        mot_de_passe = getpass.getpass("Mot de passe : ")
        if mot_de_passe != getpass.getpass("Confirmation : "):
            print("Les deux mots de passe ne correspondent pas.", file=sys.stderr)
            return 1
    if not prenom:
        prenom = _demander("Prénom")
    if not nom:
        nom = _demander("Nom")

    echecs = failed_password_rules(mot_de_passe)
    if echecs:
        print(describe_password_errors(mot_de_passe), file=sys.stderr)
        return 1

    compte, cree = creer_super_admin(email, mot_de_passe, nom, prenom)
    if cree:
        print(f"Compte d'administration créé : {compte.email} (id {compte.id_compte}).")
        print(f"Profil médecin rattaché     : id {compte.id_medecin}.")
        print("Connectez-vous sur /login, puis /admin ou /dashboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())