"""Cycle de vie des comptes : inscription, validation, connexion, blocage et
réinitialisation de mot de passe.

Ces tests utilisent une vraie base SQLite en mémoire plutôt que des doublures :
le comportement à protéger est justement à cheval entre le service et SQLAlchemy
(contraintes d'unicité, transactions). Un double de session passerait à côté
d'une requête mal écrite.
"""

from datetime import timedelta

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.compte import Compte, DemandeReinitialisation
from app.models.enums import RoleCompte, StatutCompte, StatutDemandeReinit
from app.models.medecin import Medecin
from app.services import comptes as service

# `Base` est déclarée dans app.database. Les modèles sont importés pour
# qu'ils soient enregistrés dans Base.metadata : sinon create_all ne créerait
# que les tables des modules effectivement chargés, et les requêtes échoueraient
# sur une table absente.
from app.models import audit as _audit  # noqa: F401
from app.models import decision as _decision  # noqa: F401
from app.models import donnees_derivees as _donnees_derivees  # noqa: F401
from app.models import dossier as _dossier  # noqa: F401
from app.models import evaluation as _evaluation  # noqa: F401
from app.models import parcours_therapeutique as _parcours  # noqa: F401
from app.models import patient as _patient  # noqa: F401
from app.models import reference as _reference  # noqa: F401
from app.models import traitement as _traitement  # noqa: F401
from app.database import Base

# Le schéma Postgres utilise des types ENUM, que SQLite ne connaît pas : on
# remplace la création des tables par le schéma SQLAlchemy pur.
engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class Demande:
    """Objet d'inscription minimal : le service n'accède qu'à ces champs."""

    def __init__(self, **kwargs):
        self.nom = kwargs.get("nom", "Benali")
        self.prenom = kwargs.get("prenom", "Sofiane")
        self.email = kwargs.get("email", "sofiane.benali@chu.dz")
        self.password = kwargs.get("password", "MotDePasse1")
        self.telephone = kwargs.get("telephone", "0555000000")
        self.hopital = kwargs.get("hopital", "EHS Ain Taya")


def creer_admin(db, email="admin@chu.dz") -> Compte:
    admin = Compte(
        email=email,
        mot_de_passe_hash="$2b$12$placeholder",
        role=RoleCompte.super_admin,
        statut=StatutCompte.actif,
        nom="Administrateur",
        prenom="Système",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------


def test_inscription_cree_un_compte_en_attente(db):
    compte = service.inscrire_medecin(db, Demande())

    assert compte.statut is StatutCompte.en_attente
    assert compte.role is RoleCompte.medecin
    # Aucun profil clinique avant validation : c'est ce qui garantit qu'un
    # compte non validé n'a accès à aucun dossier.
    assert compte.id_medecin is None
    assert db.query(Medecin).count() == 0


def test_email_normalise_avant_enregistrement(db):
    compte = service.inscrire_medecin(db, Demande(email="  Sofiane.Benali@CHU.dz "))

    assert compte.email == "sofiane.benali@chu.dz"


def test_email_meme_differentes_majuscules_est_refuse(db):
    service.inscrire_medecin(db, Demande())

    with pytest.raises(HTTPException) as exc:
        service.inscrire_medecin(db, Demande(email="SOFIANE.BENALI@chu.dz"))

    assert exc.value.status_code == 409


def test_mot_de_passe_trop_faible_refuse(db):
    with pytest.raises(HTTPException) as exc:
        service.inscrire_medecin(db, Demande(password="court"))

    assert exc.value.status_code == 422


def test_mot_de_passe_nest_jamais_stocke_en_clair(db):
    compte = service.inscrire_medecin(db, Demande())

    assert "MotDePasse1" not in compte.mot_de_passe_hash
    assert compte.mot_de_passe_hash.startswith("$2")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_validation_cree_le_profil_avec_lidentite_declaree(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)

    accepte = service.accepter_compte(db, compte.id_compte, admin)

    assert accepte.statut is StatutCompte.actif
    assert accepte.active_par == admin.id_compte
    medecin = db.get(Medecin, accepte.id_medecin)
    assert medecin is not None
    # L'identité vient de l'inscription : l'admin valide un dossier, il ne le
    # saisit pas.
    assert (medecin.nom, medecin.prenom) == ("Benali", "Sofiane")
    assert medecin.email == "sofiane.benali@chu.dz"


def test_validation_rattache_un_profil_existant_plutot_que_de_doublon(db):
    # Cas de migration : le profil existe déjà depuis l'ancienne
    # authentification, seul le compte est nouveau.
    existant = Medecin(nom="Benali", prenom="Sofiane", email="sofiane.benali@chu.dz", telephone="", hopital="")
    db.add(existant)
    db.commit()
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)

    accepte = service.accepter_compte(db, compte.id_compte, admin)

    assert accepte.id_medecin == existant.id_medecin
    assert db.query(Medecin).count() == 1


def test_compte_deja_actif_ne_peut_pas_revalider(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)

    with pytest.raises(HTTPException) as exc:
        service.accepter_compte(db, compte.id_compte, admin)

    assert exc.value.status_code == 409


def test_compte_administration_ne_passe_pas_par_la_validation(db):
    admin = creer_admin(db)

    with pytest.raises(HTTPException) as exc:
        service.accepter_compte(db, admin.id_compte, admin)

    assert exc.value.status_code == 409


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------


def test_compte_en_attente_recoit_403_explicite(db):
    compte = service.inscrire_medecin(db, Demande())

    with pytest.raises(HTTPException) as exc:
        service.connecter(db, compte.email, "MotDePasse1")

    # 403 et non 401 : le médecin doit comprendre que son inscription est en
    # cours, pas qu'il a mal saisi ses identifiants.
    assert exc.value.status_code == 403
    assert "validation" in exc.value.detail.lower()


def test_compte_bloque_recoit_403_avec_son_motif(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.bloquer_compte(db, compte.id_compte, admin, "Faux diplome")

    with pytest.raises(HTTPException) as exc:
        service.connecter(db, compte.email, "MotDePasse1")

    assert exc.value.status_code == 403
    assert "Faux diplome" in exc.value.detail


def test_email_inconnu_et_mot_de_passe_faux_donnent_la_meme_reponse(db):
    service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    compte = db.query(Compte).filter(Compte.role == RoleCompte.medecin).one()
    service.accepter_compte(db, compte.id_compte, admin)

    with pytest.raises(HTTPException) as inconnu:
        service.connecter(db, "inconnu@chu.dz", "MotDePasse1")
    with pytest.raises(HTTPException) as mauvais:
        service.connecter(db, compte.email, "MauvaisMotDePasse1")

    # Deux réponses identiques : sinon la page de connexion permet de lister
    # les médecins inscrits.
    assert inconnu.value.status_code == mauvais.value.status_code == 401
    assert inconnu.value.detail == mauvais.value.detail


def test_connexion_reussie_reinitialise_le_registre_d_echecs(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    compte.tentatives_echouees = 3

    service.connecter(db, compte.email, "MotDePasse1")

    assert compte.tentatives_echouees == 0
    assert compte.date_derniere_connexion is not None


def test_echecs_repetes_verrouillent_le_compte(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)

    for _ in range(5):
        with pytest.raises(HTTPException) as exc:
            service.connecter(db, compte.email, "MauvaisMotDePasse1")
        if exc.value.status_code != 401:
            break

    db.refresh(compte)
    assert compte.verrouille_jusqu_a is not None

    # Même avec le bon mot de passe : c'est tout l'intérêt du verrouillage.
    with pytest.raises(HTTPException) as exc:
        service.connecter(db, compte.email, "MotDePasse1")
    assert exc.value.status_code == 429


# ---------------------------------------------------------------------------
# Blocage / déblocage
# ---------------------------------------------------------------------------


def test_administrateur_ne_peut_pas_etre_bloque(db):
    admin = creer_admin(db)

    with pytest.raises(HTTPException) as exc:
        service.bloquer_compte(db, admin.id_compte, admin, "invalide")

    # Aucun super admin de secours n'existe pour le débloquer.
    assert exc.value.status_code == 409


def test_blocage_annule_les_demandes_de_reinitialisation_en_cours(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)

    service.bloquer_compte(db, compte.id_compte, admin, None)

    demande = db.query(DemandeReinitialisation).one()
    # Sans cela, l'admin traiterait une demande impossible à satisfaire.
    assert demande.statut is StatutDemandeReinit.annulee


def test_deblocage_d_un_compte_jamais_active_redemande_validation(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.bloquer_compte(db, compte.id_compte, admin, "incident")

    debloque = service.debloquer_compte(db, compte.id_compte)

    # Il avait été validé avant : il retrouve son accès clinique.
    assert debloque.statut is StatutCompte.actif
    assert debloque.motif_blocage is None


def test_deblocage_d_un_compte_non_valide_le_remet_en_attente(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    # On simule le cas d'un compte bloqué alors qu'il était encore en attente.
    compte.date_activation = None
    compte.statut = StatutCompte.bloque
    db.commit()

    debloque = service.debloquer_compte(db, compte.id_compte)

    assert debloque.statut is StatutCompte.en_attente


# ---------------------------------------------------------------------------
# Mot de passe oublié
# ---------------------------------------------------------------------------


def test_demande_ignoree_pour_compte_inconnu(db):
    assert service.demander_reinitialisation(db, "inconnu@chu.dz") is None


def test_demande_ignoree_pour_compte_en_attente(db):
    compte = service.inscrire_medecin(db, Demande())

    assert service.demander_reinitialisation(db, compte.email) is None


def test_demande_ne_s_accumule_pas(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)

    service.demander_reinitialisation(db, compte.email)
    service.demander_reinitialisation(db, compte.email)

    # Relancer la procédure ne doit pas empiler des lignes que l'admin
    # traiterait à l'aveugle.
    assert db.query(DemandeReinitialisation).count() == 1


def test_lien_ne_pas_pour_compte_bloque(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    demande = db.query(DemandeReinitialisation).one()
    service.bloquer_compte(db, compte.id_compte, admin, "incident")
    demande.statut = StatutDemandeReinit.en_attente
    db.commit()

    with pytest.raises(HTTPException) as exc:
        service.generer_lien_reinitialisation(db, compte.id_compte, admin)

    # Le mot de passe serait changé mais la connexion resterait refusée : mieux
    # vaut renvoyer l'admin vers « Débloquer ».
    assert exc.value.status_code == 409


def test_lien_delivre_une_url_utilisable(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)

    lien, demande = service.generer_lien_reinitialisation(db, compte.id_compte, admin)

    assert "/reset-password?jeton=" in lien
    # La base ne conserve que l'empreinte : une fuite de la table ne permet pas
    # de réinitialiser un compte.
    assert demande.jeton_hash not in lien
    assert demande.expire_le is not None


def test_jeton_permet_de_reinitialiser_une_seule_fois(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    lien, _ = service.generer_lien_reinitialisation(db, compte.id_compte, admin)
    jeton = lien.split("jeton=")[1]

    service.reinitialiser_mot_de_passe(db, jeton, "NouveauMdp1")

    assert service.connecter(db, compte.email, "NouveauMdp1")
    with pytest.raises(HTTPException) as exc:
        service.reinitialiser_mot_de_passe(db, jeton, "EncoreUnAutre1")
    # Un lien intercepté ne doit pas pouvoir être rejoué.
    assert exc.value.status_code == 400


def test_jeton_expire_est_refuse(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    lien, demande = service.generer_lien_reinitialisation(db, compte.id_compte, admin)
    demande.expire_le = demande.date_demande - timedelta(minutes=1)
    db.commit()
    jeton = lien.split("jeton=")[1]

    with pytest.raises(HTTPException) as exc:
        service.reinitialiser_mot_de_passe(db, jeton, "NouveauMdp1")

    assert "expir" in exc.value.detail.lower()


def test_jeton_inconnu_donne_la_meme_reponse_que_jeton_utilise(db):
    # La page de réinitialisation ne doit pas devenir un moyen de tester des
    # jetons au hasard.
    with pytest.raises(HTTPException) as inconnu:
        service.reinitialiser_mot_de_passe(db, "jeton-invente", "NouveauMdp1")

    assert inconnu.value.status_code == 400


def test_reinitialisation_exige_un_mot_de_passe_conforme(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    lien, _ = service.generer_lien_reinitialisation(db, compte.id_compte, admin)

    with pytest.raises(HTTPException) as exc:
        service.reinitialiser_mot_de_passe(db, lien.split("jeton=")[1], "faible")

    assert exc.value.status_code == 422


# ---------------------------------------------------------------------------
# Mot de passe provisoire posé par l'admin
# ---------------------------------------------------------------------------


def test_mot_de_passe_temporaire_oblige_a_un_changement(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)

    service.definir_mot_de_passe_temporaire(db, compte.id_compte, "Provisoire1")

    assert compte.doit_changer_mdp is True
    assert compte.statut is StatutCompte.actif

    _, jeton = service.connecter(db, compte.email, "Provisoire1")
    assert jeton

    service.changer_mot_de_passe(db, compte, "Provisoire1", "Personnel9")
    assert compte.doit_changer_mdp is False


def test_changement_exige_le_bon_ancien_mot_de_passe(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.definir_mot_de_passe_temporaire(db, compte.id_compte, "Provisoire1")

    with pytest.raises(HTTPException) as exc:
        service.changer_mot_de_passe(db, compte, "MauvaisAncien1", "Personnel9")

    assert exc.value.status_code == 400


def test_mot_de_passe_temporaire_refuse_pour_un_administrateur(db):
    admin = creer_admin(db)

    with pytest.raises(HTTPException) as exc:
        service.definir_mot_de_passe_temporaire(db, admin.id_compte, "Provisoire1")

    assert exc.value.status_code == 409


# ---------------------------------------------------------------------------
# Clôture d'une demande
# ---------------------------------------------------------------------------


def test_cloture_detruit_le_jeton(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    demande = db.query(DemandeReinitialisation).one()

    service.cloturer_demande(db, demande.id_demande, admin, StatutDemandeReinit.annulee)

    # Un lien oublié sur le papier ne doit pas rester valable.
    assert demande.jeton_hash is None
    assert demande.expire_le is None


def test_demande_cloturee_ne_peut_pas_recloturer(db):
    compte = service.inscrire_medecin(db, Demande())
    admin = creer_admin(db)
    service.accepter_compte(db, compte.id_compte, admin)
    service.demander_reinitialisation(db, compte.email)
    demande = db.query(DemandeReinitialisation).one()
    service.cloturer_demande(db, demande.id_demande, admin, StatutDemandeReinit.traitee)

    with pytest.raises(HTTPException) as exc:
        service.cloturer_demande(db, demande.id_demande, admin, StatutDemandeReinit.annulee)

    assert exc.value.status_code == 409


# ---------------------------------------------------------------------------
# Statistiques
# ---------------------------------------------------------------------------


def test_statistiques_comptent_par_statut(db):
    admin = creer_admin(db)
    attente = service.inscrire_medecin(db, Demande())
    actif = service.inscrire_medecin(db, Demande(email="second@chu.dz"))
    bloque = service.inscrire_medecin(db, Demande(email="trois@chu.dz"))
    service.accepter_compte(db, actif.id_compte, admin)
    service.accepter_compte(db, bloque.id_compte, admin)
    service.bloquer_compte(db, bloque.id_compte, admin, "incident")

    stats = service.statistiques(db)

    assert stats["total_comptes"] == 4  # 3 médecins + 1 administrateur
    assert stats["comptes_en_attente"] == 1
    assert stats["comptes_actifs"] == 2  # le médecin + l'administrateur
    assert stats["comptes_bloques"] == 1
    assert attente.id_compte != actif.id_compte


# ---------------------------------------------------------------------------
# Mode développement sans authentification
# ---------------------------------------------------------------------------


def test_compte_demo_demande_est_relie_a_un_profil_medecin(db, monkeypatch):
    from app.dependencies import _compte_demo

    compte = _compte_demo(db)

    # Toutes les routes cliniques passent par get_medecin_for_user, qui refuse
    # un compte sans profil. Un compte démo non rattaché rendait donc
    # DISABLE_AUTH=True inutilisable sur le moindre dossier patient.
    assert compte.id_medecin is not None
    assert db.get(Medecin, compte.id_medecin) is not None
    assert compte.statut is StatutCompte.actif


def test_compte_demo_est_reutilise_d_une_requete_a_l_autre(db):
    from app.dependencies import _compte_demo

    premier = _compte_demo(db)
    second = _compte_demo(db)

    assert premier.id_compte == second.id_compte
    assert db.query(Medecin).count() == 1
