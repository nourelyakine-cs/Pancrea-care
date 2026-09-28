import enum

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class StatutDossier(str, enum.Enum):
    ouvert = "ouvert"
    clos = "clos"
    archive = "archive"


class DossierPatient(Base):
    __tablename__ = "dossier_patient"

    id_dossier = Column(Integer, primary_key=True, index=True)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="RESTRICT"), nullable=False)
    id_medecin_referent = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    statut = Column(
        Enum(
            StatutDossier,
            name="t_statut_dossier",
            create_type=False
        ),
        nullable=False,
        default=StatutDossier.ouvert
    )

    patient = relationship("Patient")
    medecin_referent = relationship("Medecin")


class DegreParente(str, enum.Enum):
    premier_degre = "premier_degre"
    deuxieme_degre = "deuxieme_degre"
    troisieme_degre_ou_plus = "troisieme_degre_ou_plus"
    inconnu = "inconnu"


class AntecedentFamilial(Base):
    __tablename__ = "antecedent_familial"

    id_antecedent = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    degre_parente = Column(
        Enum(
            DegreParente,
            name="t_degre_parente",
            create_type=False
        ),
        default=DegreParente.inconnu
    )
    nombre_apparentes = Column(SmallInteger, default=1)
    type_cancer = Column(String(80), default="pancreas")

    dossier = relationship("DossierPatient")


class StatutMutation(str, enum.Enum):
    mute = "mute"
    non_mute = "non_mute"


class MutationGerminale(Base):
    __tablename__ = "mutation_germinale"

    id_mutation = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    id_gene = Column(Integer, ForeignKey("gene.id_gene"), nullable=False)
    statut = Column(
        Enum(
            StatutMutation,
            name="t_statut_mutation",
            create_type=False
        ),
        nullable=False,
        default=StatutMutation.mute
    )
    date_test = Column(Date)

    dossier = relationship("DossierPatient")
    gene = relationship("Gene")
