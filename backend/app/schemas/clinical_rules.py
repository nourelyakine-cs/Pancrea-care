from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ClinicalRulesCalculateRequest(BaseModel):
    categorie_t: str = Field(description="T1a, T1b, T1c, T2, T3 ou T4")
    categorie_n: str = Field(description="N0, N1 ou N2")
    categorie_m: str | None = Field(default=None, description="M0/M1; inféré de l'imagerie si absent")
    version_moteur: str = Field(default="tncd-2024-v1", max_length=20)


class DonneesDeriveesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_derive: int
    id_evaluation: int
    version_moteur: str
    source_code: str
    source_version: str
    date_calcul: datetime
    resecabilite: str | None
    categorie_t: str | None
    categorie_n: str | None
    categorie_m: str | None
    stade_global: str | None
    critere_abc_a: str | None
    critere_abc_b: bool | None
    critere_abc_c: bool | None
    sous_categorie_abc: str | None
    justification_calcul: str | None


# --- Explicabilité du moteur de règles (GET .../recommendations) ---------------


class RecommendationItem(BaseModel):
    """Une recommandation déclenchée par une règle (R01-R18, T1-T4...)."""

    code: str = Field(description="Code de la règle déclenchée, ex. 'R01', 'T3'")
    conclusion: str = Field(description="Justification clinique textuelle de la recommandation")
    reference: str = Field(description="Référence TNCD justifiant la règle")
    grade: str = Field(description="Niveau de preuve : 'A', 'B' ou 'accord_experts'")
    criteres_evalues: dict[str, Any] = Field(
        description="Valeurs des faits patient qui ont déclenché cette règle"
    )


class DecisionPathStep(BaseModel):
    """Une étape du chemin de décision : le résultat de l'évaluation d'UNE règle,
    qu'elle ait été déclenchée, non déclenchée, ou ignorée faute de données."""

    code: str = Field(description="Code de la règle évaluée")
    statut: str = Field(description="'declenchee', 'non_declenchee' ou 'ignoree'")
    motif: str | None = Field(default=None, description="Raison si la règle a été ignorée")
    champs_manquants: list[str] | None = Field(
        default=None, description="Faits manquants ayant empêché l'évaluation"
    )
    reference: str | None = Field(default=None, description="Référence TNCD de la règle")
    grade: str | None = Field(default=None, description="Niveau de preuve de la règle")
    criteres_evalues: dict[str, Any] | None = Field(
        default=None, description="Valeurs des faits patient examinées par cette règle"
    )
    nombre_conclusions: int | None = Field(
        default=None, description="Nombre de recommandations produites par cette règle"
    )


class RecommendationsResponse(BaseModel):
    """Réponse de GET /clinical-rules/evaluations/{id_evaluation}/recommendations."""

    facts: dict[str, Any] = Field(description="Faits cliniques utilisés en entrée du moteur")
    recommendations: list[RecommendationItem] = Field(
        description="Recommandations produites par les règles déclenchées"
    )
    regles_declenchees: list[str] = Field(
        description="Codes des règles déclenchées, ex. ['R01', 'T3']"
    )
    decision_path: list[DecisionPathStep] = Field(
        description="Chemin de décision complet : ordre et résultat de l'évaluation de chaque règle"
    )
