from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

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


class ProtocoleContexte(Base):
    __tablename__ = "protocole_contexte"

    id_protocole = Column(
        Integer,
        ForeignKey("protocole_traitement.id_protocole", ondelete="CASCADE"),
        primary_key=True,
    )
    contexte_usage = Column(String(30), primary_key=True)

    protocole = relationship("ProtocoleTraitement")


class SourceReferentiel(Base):
    __tablename__ = "source_referentiel"

    id_source = Column(Integer, primary_key=True, index=True)
    code = Column(String(40), unique=True, nullable=False)
    titre = Column(String(200))
    version = Column(String(50))
    date_publication = Column(Date)
