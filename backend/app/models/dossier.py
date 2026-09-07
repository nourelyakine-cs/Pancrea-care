from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class DossierPatient(Base):
    __tablename__ = "dossier_patient"

    id_dossier = Column(Integer, primary_key=True, index=True)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="RESTRICT"), nullable=False)
    id_medecin_referent = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    statut = Column(String(20), nullable=False, server_default="ouvert")

    patient = relationship("Patient")
    medecin_referent = relationship("Medecin")


class AntecedentFamilial(Base):
    __tablename__ = "antecedent_familial"

    id_antecedent = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    degre_parente = Column(String(30), default="inconnu")
    nombre_apparentes = Column(SmallInteger, default=1)
    type_cancer = Column(String(80), default="pancreas")

    dossier = relationship("DossierPatient")


class MutationGerminale(Base):
    __tablename__ = "mutation_germinale"

    id_mutation = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    id_gene = Column(Integer, ForeignKey("gene.id_gene"), nullable=False)
    statut = Column(String(20), nullable=False, default="mute")
    date_test = Column(Date)

    dossier = relationship("DossierPatient")
    gene = relationship("Gene")
