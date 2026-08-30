from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class JournalAudit(Base):
    __tablename__ = "journal_audit"

    id_journal = Column(Integer, primary_key=True, index=True)
    id_medecin = Column(Integer, ForeignKey("medecin.id_medecin", ondelete="SET NULL"))
    action = Column(String(40))
    type_entite = Column(String(40))
    id_entite = Column(Integer)
    detail = Column(JSON)
    date_action = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    medecin = relationship("Medecin")
