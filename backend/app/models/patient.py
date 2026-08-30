from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Patient(Base):
    __tablename__ = "patient"

    id_patient = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date)
    sexe = Column(String(20), default="inconnu")
    telephone = Column(String(30))
    email = Column(String(255))
    adresse = Column(String(255))
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
