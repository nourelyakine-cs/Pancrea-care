from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Reponse


class Traitement(Base):
    __tablename__ = "traitement"

    id_traitement = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossier_patient.id_dossier", ondelete="CASCADE"), nullable=False)
    id_protocole = Column(Integer, ForeignKey("protocole_traitement.id_protocole"))
    numero_ligne = Column(SmallInteger)
    date_debut = Column(Date)
    date_fin = Column(Date)
    reponse = Column(Enum(Reponse, name="t_reponse", schema="public", native_enum=True, create_type=False, validate_strings=True))
    toxicite_residuelle = Column(Boolean, default=False)
    type_toxicite = Column(String(120))
    termine_comme_prevu = Column(Boolean)
    notes = Column(Text)

    dossier = relationship("DossierPatient")
    protocole = relationship("ProtocoleTraitement")
