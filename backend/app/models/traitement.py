from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Traitement(Base):
    __tablename__ = "traitement"

    id_traitement = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    id_protocole = Column(Integer, ForeignKey("protocole_traitement.id_protocole"))
    numero_ligne = Column(SmallInteger)
    date_debut = Column(Date)
    date_fin = Column(Date)
    reponse = Column(String(20))
    toxicite_residuelle = Column(Boolean, default=False)
    type_toxicite = Column(String(120))
    termine_comme_prevu = Column(Boolean)
    notes = Column(Text)

    dossier = relationship("DossierPatient")
    protocole = relationship("ProtocoleTraitement")
