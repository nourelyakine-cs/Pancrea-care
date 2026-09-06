from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

REFERENCE_TNCD = (
    "TNCD Chapitre 9 - Cancer du pancréas, version du 17/05/2024, "
    "section 9.2.5, Tableau IV (classification NCCN 2015 / Isaji et al., 2018)"
)


# ---------------------------------------------------------------------------
# Statuts
# ---------------------------------------------------------------------------

class StatutResecabilite(str, Enum):
    RESECABLE = "resecable"
    BORDERLINE = "borderline"
    LOCALEMENT_AVANCE = "localement_avance"
    INDETERMINE = "indetermine"  # données insuffisantes -> nécessite relecture RCP
    NON_PERTINENT_METASTATIQUE = "non_pertinent_metastatique"  # cf. étape 3 : M1 -> bascule vers la branche métastatique


# Ordre de priorité pour le calcul du statut global : on renvoie le premier
# statut de cette liste présent parmi les 4 vaisseaux. Une atteinte
# Localement Avancée est définitive et prime sur tout le reste ; une donnée
# manquante (INDETERMINE) prime sur Borderline/Résécable car elle empêche
# de conclure positivement.
_PRIORITE = [
    StatutResecabilite.LOCALEMENT_AVANCE,
    StatutResecabilite.INDETERMINE,
    StatutResecabilite.BORDERLINE,
    StatutResecabilite.RESECABLE,
]


# ---------------------------------------------------------------------------
# Modèles d'entrée (un par type de vaisseau, car la logique diffère)
# ---------------------------------------------------------------------------

class ContactArterielSimple(BaseModel):
    """AMS et tronc cœliaque (TC) : classification basée uniquement sur la
    présence de contact et le seuil de circonférence à 180° (Tableau IV)."""

    contact_present: bool = Field(
        ..., description="Contact tumeur-vaisseau visible au scanner/IRM"
    )
    circonference_ge_180: Optional[bool] = Field(
        None,
        description=(
            "True si circonférence de contact >= 180°, False si < 180°. "
            "Obligatoire si contact_present=True, ignoré sinon."
        ),
    )

    @model_validator(mode="after")
    def _coherence(self) -> "ContactArterielSimple":
        if not self.contact_present and self.circonference_ge_180 is not None:
            # On ne bloque pas, mais l'info est incohérente/inutile : on la neutralise.
            object.__setattr__(self, "circonference_ge_180", None)
        return self


class ContactArtereHepatiqueCommune(BaseModel):
    """AHC : le Tableau IV ne raisonne pas en degrés de circonférence mais en
    caractère "court" du contact, extension au TC/origine de l'AHC, et
    reconstructibilité chirurgicale."""

    contact_present: bool
    contact_court: Optional[bool] = Field(
        None,
        description="Contact de courte longueur, quel que soit le degré de circonférence",
    )
    extension_tronc_coeliaque_ou_origine_ahc: Optional[bool] = Field(
        None, description="Extension tumorale au tronc cœliaque ou à l'origine de l'AHC"
    )
    chirurgicalement_reconstructible: Optional[bool] = Field(
        None, description="Avis chirurgical : reconstruction vasculaire jugée possible"
    )


class ContactVeineuxVmsVp(BaseModel):
    """Axe veine mésentérique supérieure / veine porte (VMS/VP)."""

    contact_present: bool
    circonference_ge_180: Optional[bool] = None
    irregularite_ou_retrecissement_calibre: Optional[bool] = Field(
        None, description="Irrégularité de calibre veineux, sans occlusion"
    )
    occlusion_tumorale: Optional[bool] = None
    chirurgicalement_reconstructible: Optional[bool] = Field(
        None, description="Renseigné uniquement si occlusion_tumorale=True"
    )
    envahissement_veines_jejunales_principales: Optional[bool] = None


class ContexteClinique(BaseModel):
    """Informations contextuelles qui ne changent PAS le calcul du statut
    (le Tableau IV ne les mentionne pas explicitement) mais qui déclenchent
    des alertes informatives explicitement documentées ailleurs dans le
    TNCD (section 9.2.5)."""

    localisation_tumeur: Optional[str] = Field(
        None, description="'tete_crochet' ou 'corps_queue' (cf. Tableau I)"
    )
    tipmp_degeneree: bool = False
    atteinte_artere_splenique: bool = False
    atteinte_veine_splenique: bool = False
    variante_artere_hepatique_droite: bool = False


class ImagerieVasculaireInput(BaseModel):
    """Entrée complète du moteur. À terme, un adaptateur côté API convertira
    une ligne de la table `imagerie_vasculaire` vers ce modèle.

    `metastases` et `adenopathie_distance` ne sont pas des critères vasculaires
    au sens strict du Tableau IV, mais interviennent en correction finale du
    champ pivot `resecabilite_anatomique` (étape 3, cf. TNCD 9.2.5 p.15 pour
    l'adénopathie à distance, et la structure TNM pour le statut M).
    """

    ams: ContactArterielSimple
    tronc_coeliaque: ContactArterielSimple
    artere_hepatique_commune: ContactArtereHepatiqueCommune
    vms_vp: ContactVeineuxVmsVp
    metastases: bool = Field(
        False,
        description=(
            "Statut M1. Si True, la résécabilité anatomique locale n'est plus "
            "pertinente : bascule vers la prise en charge métastatique."
        ),
    )
    adenopathie_distance: bool = Field(
        False,
        description=(
            "Adénopathie à distance documentée (hile hépatique, racine du "
            "mésentère, rétropéritonéale ou inter-aortico-cave) — distincte de "
            "l'adénopathie régionale de la loge pancréatique, qui elle ne "
            "déclenche aucune correction (TNCD 9.2.5)."
        ),
    )
    contexte: Optional[ContexteClinique] = None


# ---------------------------------------------------------------------------
# Modèles de sortie
# ---------------------------------------------------------------------------

class ResultatVaisseau(BaseModel):
    vaisseau: str
    statut: StatutResecabilite
    justification: str


class ResultatResecabilite(BaseModel):
    statut_global: StatutResecabilite = Field(
        ..., description="Champ pivot final `resecabilite_anatomique`, après étapes 1+2+3"
    )
    statut_vasculaire_avant_correction: StatutResecabilite = Field(
        ...,
        description=(
            "Résultat des étapes 1+2 (grille vasculaire pure, sans métastase/"
            "adénopathie à distance). Conservé pour traçabilité, même quand la "
            "correction de l'étape 3 change le statut final."
        ),
    )
    correction_appliquee: Optional[str] = Field(
        None,
        description="Explication si l'étape 3 a modifié le statut vasculaire brut, sinon None.",
    )
    detail_par_vaisseau: List[ResultatVaisseau]
    vaisseaux_determinants: List[str] = Field(
        ..., description="Vaisseau(x) expliquant le statut_global retenu"
    )
    alertes: List[str] = Field(default_factory=list)
    reference: str = REFERENCE_TNCD


# ---------------------------------------------------------------------------
# Logique de classification par vaisseau
# ---------------------------------------------------------------------------

def _classifier_arteriel_simple(nom: str, c: ContactArterielSimple) -> ResultatVaisseau:
    if not c.contact_present:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.RESECABLE,
            justification=f"Pas de contact avec le/la {nom}.",
        )
    if c.circonference_ge_180 is None:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.INDETERMINE,
            justification=(
                f"Contact rapporté avec le/la {nom} mais circonférence de contact "
                "(seuil 180°) non renseignée."
            ),
        )
    if c.circonference_ge_180:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.LOCALEMENT_AVANCE,
            justification=f"Contact ≥ 180° avec le/la {nom}.",
        )
    return ResultatVaisseau(
        vaisseau=nom,
        statut=StatutResecabilite.BORDERLINE,
        justification=f"Contact < 180° avec le/la {nom}.",
    )


def _classifier_ahc(c: ContactArtereHepatiqueCommune) -> ResultatVaisseau:
    nom = "artère hépatique commune (AHC)"

    if not c.contact_present:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.RESECABLE,
            justification="Pas de contact avec l'AHC.",
        )

    if c.chirurgicalement_reconstructible is False:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.LOCALEMENT_AVANCE,
            justification="Contact avec l'AHC jugé chirurgicalement non reconstructible.",
        )

    if c.extension_tronc_coeliaque_ou_origine_ahc:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.LOCALEMENT_AVANCE,
            justification="Extension tumorale au tronc cœliaque ou à l'origine de l'AHC.",
        )

    if c.contact_court and c.chirurgicalement_reconstructible:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.BORDERLINE,
            justification=(
                "Contact court avec l'AHC, sans extension au tronc cœliaque/origine "
                "de l'AHC, jugé chirurgicalement reconstructible."
            ),
        )

    return ResultatVaisseau(
        vaisseau=nom,
        statut=StatutResecabilite.INDETERMINE,
        justification=(
            "Contact avec l'AHC signalé mais données insuffisantes (caractère court "
            "du contact et/ou reconstructibilité chirurgicale non renseignés) pour "
            "classer automatiquement -> avis chirurgical requis, à discuter en RCP."
        ),
    )


def _classifier_vms_vp(c: ContactVeineuxVmsVp) -> ResultatVaisseau:
    nom = "axe veine mésentérique supérieure / veine porte (VMS/VP)"

    if c.envahissement_veines_jejunales_principales:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.LOCALEMENT_AVANCE,
            justification="Envahissement des principales veines jéjunales.",
        )

    if c.occlusion_tumorale:
        if c.chirurgicalement_reconstructible is False:
            return ResultatVaisseau(
                vaisseau=nom,
                statut=StatutResecabilite.LOCALEMENT_AVANCE,
                justification=(
                    "Occlusion tumorale de la VMS/VP jugée chirurgicalement non "
                    "reconstructible."
                ),
            )
        if c.chirurgicalement_reconstructible is True:
            return ResultatVaisseau(
                vaisseau=nom,
                statut=StatutResecabilite.BORDERLINE,
                justification=(
                    "Occlusion tumorale de la VMS/VP jugée chirurgicalement "
                    "reconstructible."
                ),
            )
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.INDETERMINE,
            justification=(
                "Occlusion tumorale de la VMS/VP signalée, reconstructibilité "
                "chirurgicale non renseignée."
            ),
        )

    if not c.contact_present:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.RESECABLE,
            justification="Pas de contact avec la VMS/VP.",
        )

    if c.circonference_ge_180 is None:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.INDETERMINE,
            justification="Contact avec la VMS/VP rapporté mais circonférence non renseignée.",
        )

    if c.circonference_ge_180:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.BORDERLINE,
            justification="Contact ≥ 180° avec la VMS/VP.",
        )

    # Contact < 180° : le calibre veineux (irrégularité) fait basculer en borderline
    if c.irregularite_ou_retrecissement_calibre:
        return ResultatVaisseau(
            vaisseau=nom,
            statut=StatutResecabilite.BORDERLINE,
            justification=(
                "Contact < 180° avec la VMS/VP mais irrégularité/rétrécissement du "
                "calibre veineux associé, sans occlusion."
            ),
        )

    return ResultatVaisseau(
        vaisseau=nom,
        statut=StatutResecabilite.RESECABLE,
        justification="Contact < 180° avec la VMS/VP, sans irrégularité de calibre.",
    )


# ---------------------------------------------------------------------------
# Alertes informatives (n'influencent PAS le statut, mais documentées TNCD 9.2.5)
# ---------------------------------------------------------------------------

def _generer_alertes(
    data: ImagerieVasculaireInput, resultats: List[ResultatVaisseau]
) -> List[str]:
    alertes: List[str] = []
    ctx = data.contexte

    if ctx and ctx.tipmp_degeneree:
        alertes.append(
            "TIPMP dégénérée : l'atteinte vasculaire est fréquemment surestimée dans "
            "ce contexte (TNCD 9.2.5) — à réévaluer en RCP avant de conclure à la "
            "non-résécabilité."
        )

    if ctx and (ctx.atteinte_artere_splenique or ctx.atteinte_veine_splenique):
        if ctx.localisation_tumeur == "corps_queue":
            alertes.append(
                "Atteinte de l'artère et/ou de la veine splénique : ne constitue PAS "
                "en soi une contre-indication à la résection d'emblée pour une tumeur "
                "du corps/de la queue du pancréas (TNCD 9.2.5)."
            )
        else:
            alertes.append(
                "Atteinte de l'artère et/ou de la veine splénique signalée : "
                "l'exemption prévue par le TNCD 9.2.5 ne concerne explicitement que "
                "les tumeurs du corps/de la queue — à discuter en RCP pour une "
                "tumeur céphalique."
            )

    if ctx and ctx.variante_artere_hepatique_droite:
        alertes.append(
            "Variante anatomique d'artère hépatique droite : ne contre-indique pas "
            "définitivement une tentative de résection carcinologique, mais doit "
            "être signalée à l'équipe chirurgicale (TNCD 9.4.1.1)."
        )

    if any(r.statut == StatutResecabilite.INDETERMINE for r in resultats):
        alertes.append(
            "Données vasculaires incomplètes pour au moins un vaisseau : "
            "classification automatique impossible -> relecture radiologique/"
            "chirurgicale en RCP requise avant conclusion."
        )

    if any(
        r.statut in (StatutResecabilite.BORDERLINE, StatutResecabilite.LOCALEMENT_AVANCE)
        for r in resultats
    ):
        alertes.append(
            "Toute atteinte vasculaire doit être relue en réunion de concertation "
            "pluridisciplinaire par radiologues, chirurgiens et oncologues/"
            "gastroentérologues expérimentés en pathologie bilio-pancréatique "
            "(TNCD 9.2.5)."
        )

    return alertes


# ---------------------------------------------------------------------------
# Fonction publique principale
# ---------------------------------------------------------------------------

def evaluer_resecabilite_vasculaire(data: ImagerieVasculaireInput) -> ResultatResecabilite:
    """Point d'entrée unique du moteur — calcule le champ pivot `resecabilite_anatomique`.

    Étapes 1+2 (grille vasculaire pure, Tableau IV TNCD 9.2.5) :
        Chaque vaisseau (AMS, TC, AHC, VMS/VP) est classé indépendamment, puis
        le statut le plus péjoratif des 4 est retenu.

    Étape 3 (correction finale, intégrée ici) :
        - SI metastases=True -> le statut vasculaire n'est plus pertinent,
          bascule vers NON_PERTINENT_METASTATIQUE (branche métastatique).
        - SINON SI adenopathie_distance=True -> LOCALEMENT_AVANCE, quel que
          soit le résultat vasculaire (TNCD 9.2.5, p.15 : une adénopathie à
          distance documentée contre-indique une stratégie de chirurgie
          première).
        - SINON -> le statut retenu est celui des étapes 1+2, inchangé.
      La priorité "metastases avant adenopathie_distance" reprend l'ordre du
      pseudocode source (document CDSS, Partie A.4, note technique).

    Renvoie un statut global, le statut vasculaire brut avant correction (pour
    traçabilité), le détail par vaisseau avec justification textuelle, et des
    alertes contextuelles.
    """
    resultats = [
        _classifier_arteriel_simple("artère mésentérique supérieure (AMS)", data.ams),
        _classifier_arteriel_simple("tronc cœliaque (TC)", data.tronc_coeliaque),
        _classifier_ahc(data.artere_hepatique_commune),
        _classifier_vms_vp(data.vms_vp),
    ]

    # --- Étapes 1+2 : grille vasculaire pure ---
    statut_vasculaire = next(
        (s for s in _PRIORITE if any(r.statut == s for r in resultats)),
        StatutResecabilite.RESECABLE,
    )

    # --- Étape 3 : correction métastase / adénopathie à distance ---
    statut_global = statut_vasculaire
    correction_appliquee: Optional[str] = None
    vaisseaux_determinants = [r.vaisseau for r in resultats if r.statut == statut_vasculaire]

    if data.metastases:
        statut_global = StatutResecabilite.NON_PERTINENT_METASTATIQUE
        correction_appliquee = (
            "Statut métastatique (M1) : la résécabilité anatomique locale n'est "
            "plus le critère pertinent -> prise en charge de la maladie "
            "métastatique (structure TNM, cf. Tableau III)."
        )
        vaisseaux_determinants = []
    elif data.adenopathie_distance:
        statut_global = StatutResecabilite.LOCALEMENT_AVANCE
        correction_appliquee = (
            "Adénopathie à distance documentée (hile hépatique, racine du "
            "mésentère, rétropéritonéale ou inter-aortico-cave) : contre-indique "
            "une stratégie de chirurgie première, quel que soit le statut "
            "vasculaire local (TNCD 9.2.5, p.15)."
        )
        vaisseaux_determinants = ["adénopathie à distance (hors grille vasculaire)"]

    alertes = _generer_alertes(data, resultats)
    if correction_appliquee:
        alertes.append(
            "Statut vasculaire modifié par une correction hors grille "
            f"vasculaire : {correction_appliquee}"
        )

    return ResultatResecabilite(
        statut_global=statut_global,
        statut_vasculaire_avant_correction=statut_vasculaire,
        correction_appliquee=correction_appliquee,
        detail_par_vaisseau=resultats,
        vaisseaux_determinants=vaisseaux_determinants,
        alertes=alertes,
    )


# ---------------------------------------------------------------------------
# Exemple d'intégration API (indicatif — à adapter au schéma réel de Meriem)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    exemple = ImagerieVasculaireInput(
        ams=ContactArterielSimple(contact_present=False),
        tronc_coeliaque=ContactArterielSimple(contact_present=False),
        artere_hepatique_commune=ContactArtereHepatiqueCommune(contact_present=False),
        vms_vp=ContactVeineuxVmsVp(
            contact_present=True,
            circonference_ge_180=False,
            irregularite_ou_retrecissement_calibre=True,
        ),
        metastases=False,
        adenopathie_distance=False,
        contexte=ContexteClinique(localisation_tumeur="tete_crochet"),
    )
    resultat = evaluer_resecabilite_vasculaire(exemple)
    print(resultat.model_dump_json(indent=2, ensure_ascii=False))
