from __future__ import annotations

from typing import Any

from .resecabilite_vasculaire import (
    ContactArterielSimple,
    ContactArtereHepatiqueCommune,
    ContactVeineuxVmsVp,
    ContexteClinique,
    ImagerieVasculaireInput,
)
from .staging_tnm_criteres_abc import (
    CategorieM,
    CategorieN,
    CategorieT,
    EvaluationBiologiqueCliniqueInput,
)


def _required(value: Any, field: str) -> Any:
    if value is None:
        raise ValueError(f"{field} est obligatoire pour le calcul : valeur NULL détectée")
    return value


def _contact_arteriel(value: str | None, field: str) -> ContactArterielSimple:
    value = _required(value, field)
    if value == "absent":
        return ContactArterielSimple(contact_present=False)
    if value == "lt180":
        return ContactArterielSimple(contact_present=True, circonference_ge_180=False)
    if value == "ge180":
        return ContactArterielSimple(contact_present=True, circonference_ge_180=True)
    raise ValueError(f"Valeur {field} inconnue : {value}")


def _ahc(value: str | None) -> ContactArtereHepatiqueCommune:
    value = _required(value, "contact_art_hepatique")
    if value == "absent":
        return ContactArtereHepatiqueCommune(contact_present=False)
    if value == "court_sans_envahissement":
        return ContactArtereHepatiqueCommune(
            contact_present=True,
            contact_court=True,
            extension_tronc_coeliaque_ou_origine_ahc=False,
            chirurgicalement_reconstructible=True,
        )
    if value == "envahissant":
        return ContactArtereHepatiqueCommune(
            contact_present=True,
            extension_tronc_coeliaque_ou_origine_ahc=True,
        )
    raise ValueError(f"Valeur contact_art_hepatique inconnue : {value}")


def _vms_vp(value: str | None) -> ContactVeineuxVmsVp:
    value = _required(value, "contact_vms_vp")
    if value == "absent":
        return ContactVeineuxVmsVp(contact_present=False)
    if value == "lt180_sans_irregularite":
        return ContactVeineuxVmsVp(contact_present=True, circonference_ge_180=False)
    if value == "ge180_ou_irregularite":
        return ContactVeineuxVmsVp(
            contact_present=True,
            circonference_ge_180=True,
        )
    if value == "occlusion_reconstructible":
        return ContactVeineuxVmsVp(
            contact_present=True,
            occlusion_tumorale=True,
            chirurgicalement_reconstructible=True,
        )
    if value == "occlusion_non_reconstructible":
        return ContactVeineuxVmsVp(
            contact_present=True,
            occlusion_tumorale=True,
            chirurgicalement_reconstructible=False,
        )
    raise ValueError(f"Valeur contact_vms_vp inconnue : {value}")


def image_to_engine_input(image: Any) -> ImagerieVasculaireInput:
    """Convertit une ligne ORM Imagerie en entrée strictement validée du moteur."""
    metastases = _required(image.metastases_presentes, "metastases_presentes")
    adenopathie = _required(
        image.extension_ganglionnaire_distance,
        "extension_ganglionnaire_distance",
    )
    return ImagerieVasculaireInput(
        ams=_contact_arteriel(image.contact_ams, "contact_ams"),
        tronc_coeliaque=_contact_arteriel(
            image.contact_tronc_coeliaque, "contact_tronc_coeliaque"
        ),
        artere_hepatique_commune=_ahc(image.contact_art_hepatique),
        vms_vp=_vms_vp(image.contact_vms_vp),
        metastases=metastases,
        adenopathie_distance=adenopathie,
        contexte=ContexteClinique(
            localisation_tumeur=(
                image.localisation_tumorale
                if image.localisation_tumorale != "inconnu"
                else None
            )
        ),
    )


def biology_to_engine_input(evaluation: Any, biology: Any | None) -> EvaluationBiologiqueCliniqueInput:
    if evaluation.ecog is None:
        raise ValueError("ecog est obligatoire pour le critère C : valeur NULL détectée")
    if biology is None:
        raise ValueError("biologie absente : le CA19-9 et la cholestase doivent être vérifiés")
    if biology.cholestase is None:
        raise ValueError("cholestase est obligatoire pour interpréter le critère B")
    return EvaluationBiologiqueCliniqueInput(
        ca19_9=float(biology.ca19_9) if biology.ca19_9 is not None else None,
        cholestase=biology.cholestase,
        ecog=evaluation.ecog,
    )


def parse_tnm(t: str, n: str, m: str) -> tuple[CategorieT, CategorieN, CategorieM]:
    try:
        parsed_t = CategorieT(t)
        parsed_n = CategorieN(n)
        parsed_m = CategorieM(m)
    except ValueError as exc:
        raise ValueError(f"Catégorie TNM invalide : {exc}") from exc
    if parsed_t.value == "TX" or parsed_n.value == "NX":
        raise ValueError("Impossible de calculer le stade avec T=TX ou N=NX")
    return parsed_t, parsed_n, parsed_m


def db_resecabilite_value(status: str) -> str:
    return "metastatique" if status == "non_pertinent_metastatique" else status
