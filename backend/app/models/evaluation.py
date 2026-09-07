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
import enum

from app.database import Base


class EtatNutritionnel(str, enum.Enum):
    normal = "normal"
    denutrition_moderee = "denutrition_moderee"
    denutrition_severe = "denutrition_severe"
    inconnu = "inconnu"

class Diabete(str, enum.Enum):
    absent = "absent"
    recent_moins_2ans = "recent_moins_2ans"
    ancien = "ancien"
    inconnu = "inconnu"



class EvaluationClinique(Base):
    __tablename__ = "evaluation_clinique"

    id_evaluation = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="RESTRICT"), nullable=False)
    id_medecin_evaluateur = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))
    date_evaluation = Column(Date, nullable=False)
    contexte = Column(
    Enum(
        "diagnostic",
        "pre_neoadjuvant",
        "restaging",
        "pre_chirurgie",
        "adjuvant",
        "surveillance",
        "recidive",
        name="t_contexte_evaluation",
        create_type=False
    ),
    default="diagnostic"
    )
    ecog = Column(SmallInteger)
    etat_nutritionnel = Column(
    Enum(
        EtatNutritionnel,
        name="t_etat_nutritionnel",
        create_type=False
    ),
    default=EtatNutritionnel.inconnu
    )
    douleur_presente = Column(Boolean)
    intensite_douleur = Column(SmallInteger)
    ictere = Column(Boolean)
    diabete = Column(
    Enum(
        Diabete,
        name="t_diabete",
        create_type=False
    ),
    default=Diabete.inconnu
    )
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


class StatutLewis(str, enum.Enum):
    exprime = "exprime"
    a_b_negatif = "a_b_negatif"
    inconnu = "inconnu"


class StatutDpd(str, enum.Enum):
    normal = "normal"
    deficit_partiel = "deficit_partiel"
    deficit_complet = "deficit_complet"
    non_teste = "non_teste"

class Biologie(Base):
    __tablename__ = "biologie"

    id_biologie = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    ca19_9 = Column(Numeric(10, 2))
    ca19_9_multiple_lsn = Column(Numeric(8, 2))
    cholestase = Column(Boolean)
    bilirubine = Column(Numeric(8, 2))
    bilirubine_ratio_lsn = Column(Numeric(6, 2))
    statut_lewis = Column(
    Enum(
        StatutLewis,
        name="t_statut_lewis",
        create_type=False
    ),
    default=StatutLewis.inconnu
    )

    statut_dpd = Column(
        Enum(
            StatutDpd,
            name="t_statut_dpd",
            create_type=False
        ),
        default=StatutDpd.non_teste
    )
    albuminemie = Column(Numeric(5, 2))
    date_analyse = Column(Date)

    evaluation = relationship("EvaluationClinique")

class TypeImagerie(str, enum.Enum):
    TDM = "TDM"
    IRM = "IRM"


class LocalisationTumorale(str, enum.Enum):
    tete_crochet = "tete_crochet"
    corps_queue = "corps_queue"
    inconnu = "inconnu"


class ContactVaisseau(str, enum.Enum):
    absent = "absent"
    lt180 = "lt180"
    ge180 = "ge180"


class ContactArtHepatique(str, enum.Enum):
    absent = "absent"
    court_sans_envahissement = "court_sans_envahissement"
    envahissant = "envahissant"


class ContactVmsVp(str, enum.Enum):
    absent = "absent"
    lt180_sans_irregularite = "lt180_sans_irregularite"
    ge180_ou_irregularite = "ge180_ou_irregularite"
    occlusion_reconstructible = "occlusion_reconstructible"
    occlusion_non_reconstructible = "occlusion_non_reconstructible"

class Imagerie(Base):
    __tablename__ = "imagerie"

    id_imagerie = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_evaluation = Column(
        Integer,
        ForeignKey(
            "evaluation_clinique.id_evaluation",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    type_imagerie = Column(
        Enum(
            TypeImagerie,
            name="t_type_imagerie",
            create_type=False
        ),
        nullable=False
    )

    date_imagerie = Column(
        Date,
        nullable=False
    )

    localisation_tumorale = Column(
        Enum(
            LocalisationTumorale,
            name="t_localisation_tumorale",
            create_type=False
        ),
        default=LocalisationTumorale.inconnu
    )

    taille_tumorale_cm = Column(
        Numeric(5, 2)
    )

    contact_ams = Column(
        Enum(
            ContactVaisseau,
            name="t_contact_vaisseau",
            create_type=False
        )
    )

    contact_tronc_coeliaque = Column(
        Enum(
            ContactVaisseau,
            name="t_contact_vaisseau",
            create_type=False
        )
    )

    contact_art_hepatique = Column(
        Enum(
            ContactArtHepatique,
            name="t_contact_art_hepatique",
            create_type=False
        )
    )

    contact_vms_vp = Column(
        Enum(
            ContactVmsVp,
            name="t_contact_vms_vp",
            create_type=False
        )
    )

    extension_ganglionnaire_regionale = Column(
        Boolean,
        default=False
    )

    extension_ganglionnaire_distance = Column(
        Boolean
    )

    metastases_presentes = Column(
        Boolean
    )

    evaluation = relationship("EvaluationClinique")


class MetastaseLocalisation(Base):
    __tablename__ = "metastase_localisation"

    id_metastase = Column(Integer, primary_key=True, index=True)
    id_imagerie = Column(Integer, ForeignKey("imagerie.id_imagerie", ondelete="CASCADE"), nullable=False)
    site = Column(String(20), nullable=False)
    detail = Column(Text)

    imagerie = relationship("Imagerie")


class StatutBrca(str, enum.Enum):
    mute = "mute"
    non_mute = "non_mute"
    non_teste = "non_teste"


class StatutKras(str, enum.Enum):
    sauvage = "sauvage"
    g12c = "g12c"
    g12d = "g12d"
    g12v = "g12v"
    autre_mute = "autre_mute"
    non_teste = "non_teste"


class StatutMsi(str, enum.Enum):
    mss = "mss"
    msi_h = "msi_h"
    dmmr = "dmmr"
    non_teste = "non_teste"


class Fusion(str, enum.Enum):
    positif = "positif"
    negatif = "negatif"
    non_teste = "non_teste"

class HistologieBiologie(Base):
    __tablename__ = "histologie_biologie"

    id_histo = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False)
    preuve_histologique = Column(Boolean, default=False)
    statut_brca_germinal = Column(
    Enum(
        StatutBrca,
        name="t_statut_brca",
        create_type=False
    ),
    default=StatutBrca.non_teste
    )

    statut_kras = Column(
        Enum(
            StatutKras,
            name="t_statut_kras",
            create_type=False
        ),
        default=StatutKras.non_teste
    )

    statut_msi_dmmr = Column(
        Enum(
            StatutMsi,
            name="t_statut_msi",
            create_type=False
        ),
        default=StatutMsi.non_teste
    )

    fusion_ntrk = Column(
        Enum(
            Fusion,
            name="t_fusion",
            create_type=False
        ),
        default=Fusion.non_teste
    )

    fusion_nrg1 = Column(
        Enum(
            Fusion,
            name="t_fusion",
            create_type=False
        ),
        default=Fusion.non_teste
    )

    evaluation = relationship("EvaluationClinique")

class TypeTest(str, enum.Enum):
    panel = "panel"
    germinal = "germinal"
    biopsie_liquide = "biopsie_liquide"
    ihc = "ihc"
    ngs_arn = "ngs_arn"


class ClasseEscat(str, enum.Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"
    non_classe = "non_classe"

class AnalyseMoleculaire(Base):
    __tablename__ = "analyse_moleculaire"

    id_analyse = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_evaluation = Column(
        Integer,
        ForeignKey(
            "evaluation_clinique.id_evaluation",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    type_test = Column(
        Enum(
            TypeTest,
            name="t_type_test",
            create_type=False
        )
    )

    gene = Column(
        String(50)
    )

    alteration = Column(
        String(120)
    )

    classe_escat = Column(
        Enum(
            ClasseEscat,
            name="t_classe_escat",
            create_type=False
        )
    )

    date_test = Column(
        Date
    )

    reference_rapport = Column(
        String(120)
    )

    evaluation = relationship("EvaluationClinique")
