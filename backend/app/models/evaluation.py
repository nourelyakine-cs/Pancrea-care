from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    Enum,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class EvaluationClinique(Base):
    __tablename__ = "evaluation_clinique"

    id_evaluation = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="RESTRICT"), nullable=False)
    id_medecin_evaluateur = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))
    date_evaluation = Column(Date, nullable=False)
    contexte = Column(String(30), default="diagnostic")
    ecog = Column(SmallInteger)
    etat_nutritionnel = Column(String(30), default="inconnu")
    douleur_presente = Column(Boolean)
    intensite_douleur = Column(SmallInteger)
    ictere = Column(Boolean)
    diabete = Column(String(20), default="inconnu")
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    dossier = relationship("DossierPatient")
    medecin_evaluateur = relationship("Medecin")


class EvaluationComorbidite(Base):
    __tablename__ = "evaluation_comorbidite"

    id_evaluation = Column(
        Integer,
        ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"),
        primary_key=True
    )

    id_comorbidite = Column(
        Integer,
        ForeignKey("comorbidite.id_comorbidite"),
        primary_key=True
    )

    severite = Column(
        Enum(
            "mineure",
            "majeure",
            name="t_severite",
            create_type=False
        ),
        default="mineure"
    )

    note = Column(Text)

    evaluation = relationship("EvaluationClinique")
    comorbidite = relationship("Comorbidite")


class Biologie(Base):
    __tablename__ = "biologie"

    id_biologie = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    ca19_9 = Column(Numeric(10, 2))
    ca19_9_multiple_lsn = Column(Numeric(8, 2))
    cholestase = Column(Boolean)
    bilirubine = Column(Numeric(8, 2))
    bilirubine_ratio_lsn = Column(Numeric(6, 2))
    statut_lewis = Column(String(20), default="inconnu")
    statut_dpd = Column(String(20), default="non_teste")
    albuminemie = Column(Numeric(5, 2))
    date_analyse = Column(Date)

    evaluation = relationship("EvaluationClinique")


class Imagerie(Base):
    __tablename__ = "imagerie"

    id_imagerie = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    type_imagerie = Column(String(10), nullable=False)
    date_imagerie = Column(Date, nullable=False)
    localisation_tumorale = Column(String(30), default="inconnu")
    taille_tumorale_cm = Column(Numeric(5, 2))
    contact_ams = Column(String(20))
    contact_tronc_coeliaque = Column(String(20))
    contact_art_hepatique = Column(String(30))
    contact_vms_vp = Column(String(40))
    extension_ganglionnaire_regionale = Column(Boolean, default=False)
    extension_ganglionnaire_distance = Column(Boolean)
    metastases_presentes = Column(Boolean)

    evaluation = relationship("EvaluationClinique")


class MetastaseLocalisation(Base):
    __tablename__ = "metastase_localisation"

    id_metastase = Column(Integer, primary_key=True, index=True)
    id_imagerie = Column(Integer, ForeignKey("imagerie.id_imagerie", ondelete="CASCADE"), nullable=False)
    site = Column(String(20), nullable=False)
    detail = Column(Text)

    imagerie = relationship("Imagerie")


class HistologieBiologie(Base):
    __tablename__ = "histologie_biologie"

    id_histo = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    preuve_histologique = Column(Boolean, default=False)
    statut_brca_germinal = Column(String(20), default="non_teste")
    statut_kras = Column(String(20), default="non_teste")
    statut_msi_dmmr = Column(String(20), default="non_teste")
    fusion_ntrk = Column(String(20), default="non_teste")
    fusion_nrg1 = Column(String(20), default="non_teste")

    evaluation = relationship("EvaluationClinique")


class AnalyseMoleculaire(Base):
    __tablename__ = "analyse_moleculaire"

    id_analyse = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    type_test = Column(String(30))
    gene = Column(String(50))
    alteration = Column(String(120))
    classe_escat = Column(String(20))
    date_test = Column(Date)
    reference_rapport = Column(String(120))

    evaluation = relationship("EvaluationClinique")
