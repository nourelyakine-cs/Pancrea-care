from sqlalchemy import Boolean, Column, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class DecisionRegleDeclenchee(Base):
    __tablename__ = "decision_regle_declenchee"

    id_declenchement = Column(Integer, primary_key=True)
    id_decision = Column(Integer, ForeignKey("decision.id_decision", ondelete="CASCADE"), nullable=False)
    id_regle = Column(Integer, ForeignKey("regle.id_regle"))
    version_regle = Column(Integer)
    a_matche = Column(Boolean, default=True)
    est_alternative = Column(Boolean, default=False)
    valeur_decisive = Column(Text)
    conditions_snapshot = Column(JSON)
    texte_conclusion = Column(Text)
    grade_preuve = Column(String(20))
    section_reference = Column(String(60))

    decision = relationship("Decision")


class DecisionExplication(Base):
    __tablename__ = "decision_explication"

    id_explication = Column(Integer, primary_key=True)
    id_decision = Column(Integer, ForeignKey("decision.id_decision", ondelete="CASCADE"), nullable=False)
    ordre_etape = Column(Integer, nullable=False)
    texte_etape = Column(Text, nullable=False)

    decision = relationship("Decision")
