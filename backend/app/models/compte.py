"""Identité d'authentification, séparée du profil clinique `medecin`.

Séparer les deux tables permet d'exister comme compte sans être encore
médecin : un compte en attente de validation n'a pas de dossier patient à
protéger, mais doit déjà pouvoir être examiné par le super admin (nom,
établissement, téléphone) pour décider s'il l'accepte.
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.enums import RoleCompte, StatutCompte, StatutDemandeReinit


class Compte(Base):
    __tablename__ = "compte"

    id_compte = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(Text, nullable=False)
    role = Column(
        Enum(RoleCompte, name="t_role_compte", values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=RoleCompte.medecin,
    )
    statut = Column(
        Enum(StatutCompte, name="t_statut_compte", values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=StatutCompte.en_attente,
    )

    # Identité déclarée à l'inscription, recopiée dans `medecin` à l'acceptation.
    # Elle vit ici parce qu'un compte en attente n'a pas encore de profil
    # médecin : sans ces colonnes, l'admin n'aurait rien à afficher pour
    # statuer sur une demande.
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    telephone = Column(String(30))
    hopital = Column(String(150))

    # NULL tant que le compte n'est pas accepté : le profil médecin (et donc
    # l'accès aux dossiers) n'existe qu'après validation par le super admin.
    id_medecin = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))

    # Vrai si le mot de passe a été posé par l'admin plutôt que choisi par le
    # médecin : il doit le changer dès sa prochaine connexion.
    doit_changer_mdp = Column(Boolean, nullable=False, default=False)
    motif_blocage = Column(Text)

    # Anti-force brute : le compte est refusé jusqu'à `verrouille_jusqu_a`
    # après MAX_TENTATIVES_CONNEXION échecs consécutifs.
    tentatives_echouees = Column(Integer, nullable=False, default=0)
    verrouille_jusqu_a = Column(DateTime(timezone=True))

    date_activation = Column(DateTime(timezone=True))
    active_par = Column(Integer, ForeignKey("compte.id_compte", ondelete="SET NULL"))
    date_derniere_connexion = Column(DateTime(timezone=True))
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # `foreign_keys` est indispensable : `demande_reinitialisation` porte deux
    # clés étrangères vers `compte` (le compte concerné, et l'admin qui a
    # traité la demande). Sans cette précision, SQLAlchemy ne sait pas quel
    # chemin emprunter et échoue au premier accès à la relation.
    demandes = relationship(
        "DemandeReinitialisation",
        back_populates="compte",
        cascade="all, delete-orphan",
        foreign_keys="DemandeReinitialisation.id_compte",
    )


class DemandeReinitialisation(Base):
    """File d'attente des mots de passe oubliés, traitée par le super admin.

    La plateforme n'a pas de service d'email : c'est l'admin qui génère le
    jeton puis le transmet au médecin. Seul l'empreinte du jeton est stockée,
    de sorte qu'une fuite de cette table ne permettrait pas de réinitialiser le
    compte de qui que ce soit.
    """

    __tablename__ = "demande_reinitialisation"

    id_demande = Column(Integer, primary_key=True, index=True)
    id_compte = Column(
        Integer, ForeignKey("compte.id_compte", ondelete="CASCADE"), nullable=False
    )
    statut = Column(
        Enum(
            StatutDemandeReinit,
            name="t_statut_demande_reinit",
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
        default=StatutDemandeReinit.en_attente,
    )
    jeton_hash = Column(Text)
    expire_le = Column(DateTime(timezone=True))
    motif = Column(Text)
    traite_par = Column(Integer, ForeignKey("compte.id_compte", ondelete="SET NULL"))
    date_demande = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_traitement = Column(DateTime(timezone=True))

    # Même ambiguïté que sur `Compte.demandes`, résolue dans l'autre sens.
    compte = relationship(
        "Compte", back_populates="demandes", foreign_keys=[id_compte]
    )