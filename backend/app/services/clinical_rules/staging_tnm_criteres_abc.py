from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field   # type: ignore

REFERENCE_TNM = (
    "TNCD Chapitre 9 - Cancer du pancréas, version du 17/05/2024, "
    "Tableaux II et III (classification TNM, AJCC 8e édition 2017)"
)
REFERENCE_ABC = (
    "TNCD Chapitre 9 - Cancer du pancréas, version du 17/05/2024, "
    "section 9.2.5 p.15 (critères ABC, Isaji et al. 2018 ; Dekker et al. 2024)"
)


# ===========================================================================
# PARTIE 1 — Staging TNM (Tableaux II et III)
# ===========================================================================

class CategorieT(str, Enum):
    T1A = "T1a"
    T1B = "T1b"
    T1C = "T1c"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"


class CategorieN(str, Enum):
    N0 = "N0"
    N1 = "N1"
    N2 = "N2"


class CategorieM(str, Enum):
    M0 = "M0"
    M1 = "M1"


class StadeGlobal(str, Enum):
    IA = "IA"
    IB = "IB"
    IIA = "IIA"
    IIB = "IIB"
    III = "III"
    IV = "IV"


# Regroupement T1a/T1b/T1c -> "T1" pour le staging (Tableau III ne distingue
# pas les sous-catégories T1a/b/c, uniquement utiles pour le Tableau II /
# la classification T détaillée).
_GROUPE_T1 = {CategorieT.T1A, CategorieT.T1B, CategorieT.T1C}


class ResultatStadeTNM(BaseModel):
    stade_global: StadeGlobal
    justification: str
    reference: str = REFERENCE_TNM


def calculer_stade_tnm(t: CategorieT, n: CategorieN, m: CategorieM) -> ResultatStadeTNM:
    """Applique le Tableau III du TNCD :

        IA  = T1,    N0,      M0
        IB  = T2,    N0,      M0
        IIA = T3,    N0,      M0
        IIB = T1-T3, N1,      M0
        III = T4,    tout N,  M0   OU   tout T, N2, M0
        IV  = tout T, tout N, M1
    """
    if m == CategorieM.M1:
        return ResultatStadeTNM(
            stade_global=StadeGlobal.IV,
            justification=(
                f"M1 (métastase à distance) -> stade IV, quels que soient "
                f"T ({t.value}) et N ({n.value})."
            ),
        )

    if t == CategorieT.T4 or n == CategorieN.N2:
        return ResultatStadeTNM(
            stade_global=StadeGlobal.III,
            justification=(
                f"M0 et (T4 et/ou N2) -> stade III (T={t.value}, N={n.value})."
            ),
        )

    if n == CategorieN.N1:
        # T4 déjà exclu par la condition précédente -> T est forcément T1-T3 ici.
        return ResultatStadeTNM(
            stade_global=StadeGlobal.IIB,
            justification=f"M0, N1, T={t.value} (T1-T3) -> stade IIB.",
        )

    # N0, M0, T ∈ {T1a/b/c, T2, T3} (T4 déjà exclu ci-dessus)
    if t in _GROUPE_T1:
        return ResultatStadeTNM(
            stade_global=StadeGlobal.IA,
            justification=f"T1 ({t.value}), N0, M0 -> stade IA.",
        )
    if t == CategorieT.T2:
        return ResultatStadeTNM(
            stade_global=StadeGlobal.IB, justification="T2, N0, M0 -> stade IB."
        )
    if t == CategorieT.T3:
        return ResultatStadeTNM(
            stade_global=StadeGlobal.IIA, justification="T3, N0, M0 -> stade IIA."
        )

    # Ne devrait jamais être atteint (toutes les combinaisons T/N/M valides
    # sont couvertes ci-dessus) ; gardé comme garde-fou explicite.
    raise ValueError(f"Combinaison T/N/M non couverte par le Tableau III : T={t}, N={n}, M={m}")


# ===========================================================================
# PARTIE 2 — Critères ABC (page 15, section 9.2.5)
# ===========================================================================

# Seuils isolés en constantes modifiables (cf. Note importante n°2 ci-dessus).
SEUIL_CA19_9_CRITERE_B: float = 500.0  # U/mL — footnote "* B CA 19-9 > 500 UI/mL"
SEUIL_ECOG_CRITERE_C: int = 2          # OMS  — footnote "** C état général OMS 2 ou plus"


class EvaluationBiologiqueCliniqueInput(BaseModel):
    ca19_9: Optional[float] = Field(
        None,
        description="CA19-9 en U/mL. None si non dosé/non renseigné.",
    )
    cholestase: bool = Field(
        False,
        description=(
            "Cholestase associée. Si True, le CA19-9 n'est pas interprétable "
            "pour le critère B (nombreux faux positifs en cas de cholestase, "
            "TNCD 9.2.2.3) -> critere_B_positif forcé à False même si "
            "CA19-9 > seuil."
        ),
    )
    ecog: int = Field(..., ge=0, le=4, description="ECOG / Performance Status (0 à 4)")


class ResultatCriteresABC(BaseModel):
    critere_B_positif: bool
    critere_C_positif: bool
    type_abc: str = Field(..., description="'A' / 'AB' / 'AC' / 'ABC'")
    ca19_9_renseigne: bool
    seuil_ca19_9_utilise: float
    seuil_ecog_utilise: int
    justification: List[str]
    reference: str = REFERENCE_ABC


def calculer_criteres_abc(
    data: EvaluationBiologiqueCliniqueInput,
    seuil_ca19_9: float = SEUIL_CA19_9_CRITERE_B,
    seuil_ecog: int = SEUIL_ECOG_CRITERE_C,
) -> ResultatCriteresABC:
    """Calcule critere_B_positif, critere_C_positif et type_abc.

    `seuil_ca19_9` et `seuil_ecog` sont exposés en paramètres (et pas figés
    en dur dans la logique) précisément parce que le seuil ECOG du critère C
    n'est pas encore tranché de façon définitive (cf. Note importante n°2).
    """
    justification: List[str] = []
    ca19_9_renseigne = data.ca19_9 is not None

    if not ca19_9_renseigne:
        critere_b = False
        justification.append(
            "CA19-9 non renseigné -> critère B considéré non positif par défaut "
            "(cohérent avec la condition 'CA19_9 non renseigné' des règles "
            "consommatrices de ce champ)."
        )
    elif data.cholestase:
        critere_b = False
        justification.append(
            f"CA19-9={data.ca19_9} U/mL mais cholestase associée -> critère B "
            "non interprétable, considéré non positif (TNCD 9.2.2.3, faux "
            "positifs du CA19-9 en contexte de cholestase)."
        )
    elif data.ca19_9 > seuil_ca19_9:
        critere_b = True
        justification.append(
            f"CA19-9={data.ca19_9} U/mL > {seuil_ca19_9} U/mL, sans cholestase "
            "-> critère B positif."
        )
    else:
        critere_b = False
        justification.append(
            f"CA19-9={data.ca19_9} U/mL ≤ {seuil_ca19_9} U/mL -> critère B non positif."
        )

    critere_c = data.ecog >= seuil_ecog
    justification.append(
        f"ECOG={data.ecog} {'≥' if critere_c else '<'} {seuil_ecog} -> critère C "
        f"{'positif' if critere_c else 'non positif'}."
    )

    if critere_b and critere_c:
        type_abc = "ABC"
    elif critere_b:
        type_abc = "AB"
    elif critere_c:
        type_abc = "AC"
    else:
        type_abc = "A"

    return ResultatCriteresABC(
        critere_B_positif=critere_b,
        critere_C_positif=critere_c,
        type_abc=type_abc,
        ca19_9_renseigne=ca19_9_renseigne,
        seuil_ca19_9_utilise=seuil_ca19_9,
        seuil_ecog_utilise=seuil_ecog,
        justification=justification,
    )


# ---------------------------------------------------------------------------
# Exemple d'utilisation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    stade = calculer_stade_tnm(CategorieT.T3, CategorieN.N1, CategorieM.M0)
    print(stade.model_dump_json(indent=2, ensure_ascii=False))

    abc = calculer_criteres_abc(
        EvaluationBiologiqueCliniqueInput(ca19_9=620, cholestase=False, ecog=1)
    )
    print(abc.model_dump_json(indent=2, ensure_ascii=False))
