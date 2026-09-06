"""
Tests unitaires : staging TNM (Tableau III) et critères ABC (p.15).
"""

import pytest

from app.services.clinical_rules.staging_tnm_criteres_abc import (
    CategorieM,
    CategorieN,
    CategorieT,
    EvaluationBiologiqueCliniqueInput,
    SEUIL_CA19_9_CRITERE_B,
    SEUIL_ECOG_CRITERE_C,
    StadeGlobal,
    calculer_criteres_abc,
    calculer_stade_tnm,
)


# ---------------------------------------------------------------------------
# Staging TNM — chaque test correspond à une ligne du Tableau III
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("t", [CategorieT.T1A, CategorieT.T1B, CategorieT.T1C])
def test_stade_ia_t1_n0_m0(t):
    r = calculer_stade_tnm(t, CategorieN.N0, CategorieM.M0)
    assert r.stade_global == StadeGlobal.IA


def test_stade_ib_t2_n0_m0():
    r = calculer_stade_tnm(CategorieT.T2, CategorieN.N0, CategorieM.M0)
    assert r.stade_global == StadeGlobal.IB


def test_stade_iia_t3_n0_m0():
    r = calculer_stade_tnm(CategorieT.T3, CategorieN.N0, CategorieM.M0)
    assert r.stade_global == StadeGlobal.IIA


@pytest.mark.parametrize("t", [CategorieT.T1A, CategorieT.T2, CategorieT.T3])
def test_stade_iib_t1_a_t3_n1_m0(t):
    r = calculer_stade_tnm(t, CategorieN.N1, CategorieM.M0)
    assert r.stade_global == StadeGlobal.IIB


def test_stade_iii_t4_n0_m0():
    """T4 seul (même N0) suffit à donner le stade III."""
    r = calculer_stade_tnm(CategorieT.T4, CategorieN.N0, CategorieM.M0)
    assert r.stade_global == StadeGlobal.III


def test_stade_iii_t4_n1_m0():
    r = calculer_stade_tnm(CategorieT.T4, CategorieN.N1, CategorieM.M0)
    assert r.stade_global == StadeGlobal.III


@pytest.mark.parametrize("t", [CategorieT.T1A, CategorieT.T2, CategorieT.T3])
def test_stade_iii_n2_quel_que_soit_t(t):
    """N2 seul (même avec T1-T3) suffit à donner le stade III."""
    r = calculer_stade_tnm(t, CategorieN.N2, CategorieM.M0)
    assert r.stade_global == StadeGlobal.III


def test_stade_iii_t4_et_n2_cumules():
    r = calculer_stade_tnm(CategorieT.T4, CategorieN.N2, CategorieM.M0)
    assert r.stade_global == StadeGlobal.III


@pytest.mark.parametrize(
    "t,n",
    [
        (CategorieT.T1A, CategorieN.N0),
        (CategorieT.T2, CategorieN.N1),
        (CategorieT.T4, CategorieN.N2),
    ],
)
def test_stade_iv_des_que_m1(t, n):
    """M1 prime sur absolument tout T/N."""
    r = calculer_stade_tnm(t, n, CategorieM.M1)
    assert r.stade_global == StadeGlobal.IV


# ---------------------------------------------------------------------------
# Critères ABC — critère B (CA19-9)
# ---------------------------------------------------------------------------

def test_ca19_9_superieur_seuil_sans_cholestase_est_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=620, cholestase=False, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.critere_B_positif is True


def test_ca19_9_egal_au_seuil_nest_pas_positif():
    """Le TNCD dit '> 500', donc 500 pile n'est PAS positif (test de la borne)."""
    data = EvaluationBiologiqueCliniqueInput(ca19_9=SEUIL_CA19_9_CRITERE_B, cholestase=False, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.critere_B_positif is False


def test_ca19_9_eleve_mais_cholestase_nest_pas_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=900, cholestase=True, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.critere_B_positif is False


def test_ca19_9_non_renseigne_nest_pas_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=None, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.critere_B_positif is False
    assert r.ca19_9_renseigne is False


# ---------------------------------------------------------------------------
# Critères ABC — critère C (ECOG)
# ---------------------------------------------------------------------------

def test_ecog_superieur_ou_egal_seuil_est_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=None, ecog=SEUIL_ECOG_CRITERE_C)
    r = calculer_criteres_abc(data)
    assert r.critere_C_positif is True


def test_ecog_juste_sous_le_seuil_nest_pas_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=None, ecog=SEUIL_ECOG_CRITERE_C - 1)
    r = calculer_criteres_abc(data)
    assert r.critere_C_positif is False


def test_seuil_ecog_est_parametrable_sans_toucher_la_structure():
    """Vérifie qu'on peut changer le seuil (ex. si le prof tranche pour ECOG≥1)
    sans modifier le code, juste l'argument."""
    data = EvaluationBiologiqueCliniqueInput(ca19_9=None, ecog=1)
    r_defaut = calculer_criteres_abc(data)  # seuil par défaut = 2
    r_seuil_1 = calculer_criteres_abc(data, seuil_ecog=1)
    assert r_defaut.critere_C_positif is False
    assert r_seuil_1.critere_C_positif is True
    assert r_seuil_1.seuil_ecog_utilise == 1


# ---------------------------------------------------------------------------
# Combinaison type_abc
# ---------------------------------------------------------------------------

def test_type_abc_a_si_aucun_critere_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=100, cholestase=False, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.type_abc == "A"


def test_type_abc_ab_si_seul_b_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=700, cholestase=False, ecog=0)
    r = calculer_criteres_abc(data)
    assert r.type_abc == "AB"


def test_type_abc_ac_si_seul_c_positif():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=100, cholestase=False, ecog=3)
    r = calculer_criteres_abc(data)
    assert r.type_abc == "AC"


def test_type_abc_abc_si_les_deux_positifs():
    data = EvaluationBiologiqueCliniqueInput(ca19_9=700, cholestase=False, ecog=3)
    r = calculer_criteres_abc(data)
    assert r.type_abc == "ABC"


def test_ecog_hors_bornes_est_rejete():
    with pytest.raises(Exception):
        EvaluationBiologiqueCliniqueInput(ca19_9=100, ecog=5)
