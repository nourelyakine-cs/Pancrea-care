from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Gene(Base):
    __tablename__ = "gene"

    id_gene = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    libelle = Column(String(120))
    syndrome = Column(String(150))
    cancers_associes = Column(Text)


class Comorbidite(Base):
    __tablename__ = "comorbidite"

    id_comorbidite = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    libelle_fr = Column(String(120))
    libelle_en = Column(String(120))


class ProtocoleTraitement(Base):
    __tablename__ = "protocole_traitement"

    id_protocole = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    libelle_fr = Column(String(120))
    libelle_en = Column(String(120))
    description = Column(Text)
