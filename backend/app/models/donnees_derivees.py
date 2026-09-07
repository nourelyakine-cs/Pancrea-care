from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.database import Base


class DonneesDerivees(Base):
    __tablename__ = "donnees_derivees"
    __table_args__ = (UniqueConstraint("id_evaluation", "version_moteur"),)

    id_derive = Column(Integer, primary_key=True, index=True)

    id_evaluation = Column(
        Integer,
        ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"),
        nullable=False,
    )

    version_moteur = Column(String(20), nullable=False)
    source_code = Column(String(20), nullable=False, default="TNCD-2024")
    source_version = Column(String(30), nullable=False, default="17/05/2024")
    date_calcul = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ENUM PostgreSQL existants
    resecabilite = Column(
        Enum(
            "resecable",
            "borderline",
            "localement_avance",
            "metastatique",
            "inconnu",
            name="t_resecabilite",
            create_type=False,
        )
    )

    categorie_t = Column(
        Enum(
            "T1a",
            "T1b",
            "T1c",
            "T2",
            "T3",
            "T4",
            "TX",
            name="t_categorie_t",
            create_type=False,
        )
    )

    categorie_n = Column(
        Enum(
            "N0",
            "N1",
            "N2",
            "NX",
            name="t_categorie_n",
            create_type=False,
        )
    )

    categorie_m = Column(
        Enum(
            "M0",
            "M1",
            name="t_categorie_m",
            create_type=False,
        )
    )

    stade_global = Column(
        Enum(
            "IA",
            "IB",
            "IIA",
            "IIB",
            "III",
            "IV",
            "inconnu",
            name="t_stade_global",
            create_type=False,
        )
    )

    critere_abc_a = Column(String(30))
    critere_abc_b = Column(Boolean)
    critere_abc_c = Column(Boolean)

    sous_categorie_abc = Column(String(15))
    justification_calcul = Column(Text)