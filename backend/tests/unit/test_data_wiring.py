from datetime import date

from app.models.evaluation import MetastaseLocalisation
from app.models.enums import SiteMetastase
from app.schemas.evaluation import ParcoursTherapeutiqueCreate
from app.schemas.full_patient import FullEvaluationCreate
from app.services.clinical_rules.recommendation_rules import r05, r14, t1, t4


def test_metastasis_model_uses_native_postgres_enum():
    column = MetastaseLocalisation.__table__.c.site
    assert column.type.name == "t_site_metastase"
    assert column.type.native_enum is True
    assert {member.value for member in SiteMetastase} == {
        "hepatique", "peritoneale", "pulmonaire", "osseuse", "autre"
    }


def test_full_evaluation_accepts_parcours_and_treatments():
    payload = FullEvaluationCreate(
        date_evaluation=date(2026, 9, 28),
        ecog=1,
        parcours=ParcoursTherapeutiqueCreate(
            angiocholite=True,
            tumeur_controlee=True,
            nouvelles_metastases=False,
            traitement_medical_prevu=True,
            chirurgie_d_emblee=False,
        ),
        traitements=[
            {
                "numero_ligne": 1,
                "reponse": "progression",
                "notes": "Gemcitabine",
            }
        ],
    )
    assert payload.parcours is not None
    assert payload.parcours.angiocholite is True
    assert payload.traitements[0].notes == "Gemcitabine"


def test_parcours_facts_can_trigger_rules():
    base = {
        "resecabilite": "borderline",
        "metastases": False,
        "tumeur_controlee": True,
        "nouvelles_metastases": False,
    }
    assert r05(base) is not None

    assert r14({
        "metastases": True,
        "statut_brca": "mute",
        "pas_de_progression_apres_16_semaines_platine": True,
    }) is not None

    assert t1({
        "ictere": True,
        "angiocholite": True,
        "bilirubine": None,
    }) is not None

    assert t4({
        "traitement_medical_prevu": True,
        "chirurgie_d_emblee": False,
        "preuve_histologique": False,
    }) is not None
