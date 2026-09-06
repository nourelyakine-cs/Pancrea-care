from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
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
    date_calcul = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resecabilite = Column(String(30))
    categorie_t = Column(String(10))
    categorie_n = Column(String(10))
    categorie_m = Column(String(10))
    stade_global = Column(String(10))
    critere_abc_a = Column(String(30))
    critere_abc_b = Column(Boolean)
    critere_abc_c = Column(Boolean)
    sous_categorie_abc = Column(String(15))
    justification_calcul = Column(Text)
