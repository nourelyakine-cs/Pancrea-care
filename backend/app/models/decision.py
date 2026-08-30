from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Decision(Base):
    __tablename__ = "decision"

    id_decision = Column(Integer, primary_key=True, index=True)
    id_evaluation = Column(Integer, ForeignKey("evaluation_clinique.id_evaluation", ondelete="RESTRICT"), nullable=False)
    date_decision = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    decide_par = Column(Integer, ForeignKey("medecin.id_medecin"))
    source_code = Column(String(20))
    source_version = Column(String(30))
    snapshot_patient = Column(JSON)
    resume = Column(Text)
    necessite_rcp = Column(Boolean, default=False)

    evaluation = relationship("EvaluationClinique")
    medecin = relationship("Medecin")
