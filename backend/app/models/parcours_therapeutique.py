from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, BigInteger, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class EvaluationParcoursTherapeutique(Base):
    __tablename__ = "evaluation_parcours_therapeutique"

    id_parcours = Column(BigInteger, primary_key=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="CASCADE"), nullable=False, index=True)
    angiocholite = Column(Boolean)
    tumeur_controlee = Column(Boolean)
    nouvelles_metastases = Column(Boolean)
    chirurgie_d_emblee = Column(Boolean)
    traitement_medical_prevu = Column(Boolean)
    pas_de_progression_apres_16_semaines_platine = Column(Boolean)
    date_reevaluation = Column(Date)
    commentaire = Column(Text)
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    evaluation = relationship("EvaluationClinique")
