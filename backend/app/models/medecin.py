from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Medecin(Base):
    __tablename__ = "medecin"

    id_medecin = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    telephone = Column(String(30))
    specialite = Column(String(100))
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
