"""Schémas du tableau de bord d'administration."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.auth import (
    describe_password_errors,
    failed_password_rules,
)


class CompteAdminRead(BaseModel):
    id_compte: int
    email: str
    nom: str
    prenom: str
    role: str
    statut: str
    telephone: str | None = None
    hopital: str | None = None
    id_medecin: int | None = None
    doit_changer_mdp: bool
    motif_blocage: str | None = None
    verrouille_jusqu_a: datetime | None = None
    date_activation: datetime | None = None
    date_derniere_connexion: datetime | None = None
    date_creation: datetime


class BlocageRequest(BaseModel):
    motif: str | None = Field(default=None, max_length=500)


class MotDePasseTemporaireRequest(BaseModel):
    nouveau_mot_de_passe: str

    @field_validator("nouveau_mot_de_passe")
    @classmethod
    def _conforme(cls, valeur: str) -> str:
        # L'admin doit voir l'erreur de mot de passe sur le champ du
        # formulaire, et non un 422 global sans message lisible.
        if failed_password_rules(valeur):
            raise ValueError(describe_password_errors(valeur))
        return valeur


class LienReinitialisationRead(BaseModel):
    id_demande: int
    lien: str
    expire_le: datetime
    message: str


class DemandeReinitialisationRead(BaseModel):
    id_demande: int
    id_compte: int
    email: str
    nom: str
    prenom: str
    hopital: str | None = None
    statut: str
    motif: str | None = None
    expire_le: datetime | None = None
    date_demande: datetime
    date_traitement: datetime | None = None


class StatistiquesRead(BaseModel):
    total_comptes: int
    comptes_actifs: int
    comptes_en_attente: int
    comptes_bloques: int
    demandes_reinitialisation_en_attente: int
    inscriptions_7_jours: int
    activations_7_jours: int
    connexions_7_jours: int