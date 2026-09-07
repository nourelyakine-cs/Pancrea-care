"""
Tests unitaires du moteur de résécabilité vasculaire.

Chaque test correspond explicitement à une cellule du Tableau IV du TNCD
(Chapitre 9, section 9.2.5, version 17/05/2024) afin de garder une
traçabilité directe entre le code et la recommandation source.
"""

from app.services.clinical_rules.resecabilite_vasculaire import (
    ContactArterielSimple,
    ContactArtereHepatiqueCommune,
    ContactVeineuxVmsVp,
    ContexteClinique,
    ImagerieVasculaireInput,
    StatutResecabilite,
    evaluer_resecabilite_vasculaire,
)


def _cas_tout_resecable(**overrides) -> ImagerieVasculaireInput:
    """Cas de base 100% résécable, que les tests modifient vaisseau par vaisseau."""
    base = dict(
        ams=ContactArterielSimple(contact_present=False),
        tronc_coeliaque=ContactArterielSimple(contact_present=False),
        artere_hepatique_commune=ContactArtereHepatiqueCommune(contact_present=False),
        vms_vp=ContactVeineuxVmsVp(contact_present=False),
    )
    base.update(overrides)
    return ImagerieVasculaireInput(**base)


# ---------------------------------------------------------------------------
# Cas de référence : aucun contact -> résécable
# ---------------------------------------------------------------------------

def test_aucun_contact_est_resecable():
    resultat = evaluer_resecabilite_vasculaire(_cas_tout_resecable())
    assert resultat.statut_global == StatutResecabilite.RESECABLE
    # Les 4 vaisseaux partagent logiquement ce statut, donc les 4 apparaissent :
    assert len(resultat.vaisseaux_determinants) == 4
    assert all(r.statut == StatutResecabilite.RESECABLE for r in resultat.detail_par_vaisseau)


# ---------------------------------------------------------------------------
# AMS (Tableau IV, ligne AMS)
# ---------------------------------------------------------------------------

def test_ams_contact_inferieur_180_est_borderline():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True, circonference_ge_180=False)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.BORDERLINE
    assert "artère mésentérique supérieure (AMS)" in resultat.vaisseaux_determinants


def test_ams_contact_superieur_ou_egal_180_est_localement_avance():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True, circonference_ge_180=True)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


def test_ams_contact_sans_circonference_est_indetermine():
    data = _cas_tout_resecable(ams=ContactArterielSimple(contact_present=True))
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.INDETERMINE


# ---------------------------------------------------------------------------
# Tronc cœliaque (même logique que l'AMS)
# ---------------------------------------------------------------------------

def test_tronc_coeliaque_contact_superieur_180_est_localement_avance():
    data = _cas_tout_resecable(
        tronc_coeliaque=ContactArterielSimple(contact_present=True, circonference_ge_180=True)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


# ---------------------------------------------------------------------------
# AHC (logique spécifique : contact court + reconstructibilité)
# ---------------------------------------------------------------------------

def test_ahc_contact_court_reconstructible_sans_extension_est_borderline():
    data = _cas_tout_resecable(
        artere_hepatique_commune=ContactArtereHepatiqueCommune(
            contact_present=True,
            contact_court=True,
            extension_tronc_coeliaque_ou_origine_ahc=False,
            chirurgicalement_reconstructible=True,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.BORDERLINE


def test_ahc_non_reconstructible_est_localement_avance():
    data = _cas_tout_resecable(
        artere_hepatique_commune=ContactArtereHepatiqueCommune(
            contact_present=True,
            chirurgicalement_reconstructible=False,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


def test_ahc_extension_tronc_coeliaque_est_localement_avance_meme_si_reconstructible():
    data = _cas_tout_resecable(
        artere_hepatique_commune=ContactArtereHepatiqueCommune(
            contact_present=True,
            contact_court=True,
            extension_tronc_coeliaque_ou_origine_ahc=True,
            chirurgicalement_reconstructible=True,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


def test_ahc_donnees_insuffisantes_est_indetermine():
    data = _cas_tout_resecable(
        artere_hepatique_commune=ContactArtereHepatiqueCommune(contact_present=True)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.INDETERMINE


# ---------------------------------------------------------------------------
# VMS/VP (logique la plus riche du tableau)
# ---------------------------------------------------------------------------

def test_vms_vp_contact_inferieur_180_sans_irregularite_est_resecable():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(contact_present=True, circonference_ge_180=False)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.RESECABLE


def test_vms_vp_contact_inferieur_180_avec_irregularite_est_borderline():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(
            contact_present=True,
            circonference_ge_180=False,
            irregularite_ou_retrecissement_calibre=True,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.BORDERLINE


def test_vms_vp_contact_superieur_ou_egal_180_est_borderline():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(contact_present=True, circonference_ge_180=True)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.BORDERLINE


def test_vms_vp_occlusion_reconstructible_est_borderline():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(
            contact_present=True,
            occlusion_tumorale=True,
            chirurgicalement_reconstructible=True,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.BORDERLINE


def test_vms_vp_occlusion_non_reconstructible_est_localement_avance():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(
            contact_present=True,
            occlusion_tumorale=True,
            chirurgicalement_reconstructible=False,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


def test_vms_vp_envahissement_veines_jejunales_est_localement_avance():
    data = _cas_tout_resecable(
        vms_vp=ContactVeineuxVmsVp(
            contact_present=True,
            envahissement_veines_jejunales_principales=True,
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


# ---------------------------------------------------------------------------
# Agrégation multi-vaisseaux et priorité INDETERMINE / LOCALEMENT_AVANCE
# ---------------------------------------------------------------------------

def test_un_seul_vaisseau_localement_avance_suffit_a_rendre_le_global_localement_avance():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True, circonference_ge_180=False),  # borderline
        tronc_coeliaque=ContactArterielSimple(contact_present=True, circonference_ge_180=True),  # LA
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE
    assert "tronc cœliaque (TC)" in resultat.vaisseaux_determinants
    assert "artère mésentérique supérieure (AMS)" not in resultat.vaisseaux_determinants


def test_localement_avance_prime_sur_indetermine():
    """Une donnée manquante ailleurs ne doit jamais 'sauver' un cas déjà LA."""
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True),  # indéterminé (pas de circonférence)
        tronc_coeliaque=ContactArterielSimple(contact_present=True, circonference_ge_180=True),  # LA
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE


def test_indetermine_prime_sur_borderline_et_resecable():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True),  # indéterminé
        vms_vp=ContactVeineuxVmsVp(contact_present=True, circonference_ge_180=True),  # borderline
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.INDETERMINE


# ---------------------------------------------------------------------------
# Alertes contextuelles (TNCD 9.2.5) — ne changent pas le statut, mais doivent
# apparaître pour guider la RCP.
# ---------------------------------------------------------------------------

def test_alerte_tipmp_degeneree():
    data = _cas_tout_resecable(
        contexte=ContexteClinique(tipmp_degeneree=True, localisation_tumeur="tete_crochet")
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert any("TIPMP" in a for a in resultat.alertes)
    # Le statut anatomique lui-même n'est pas modifié par cette alerte :
    assert resultat.statut_global == StatutResecabilite.RESECABLE


def test_alerte_atteinte_splenique_corps_queue_nuance_le_message():
    data = _cas_tout_resecable(
        contexte=ContexteClinique(
            atteinte_artere_splenique=True, localisation_tumeur="corps_queue"
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert any("ne constitue PAS" in a for a in resultat.alertes)


def test_alerte_atteinte_splenique_tete_est_plus_prudente():
    data = _cas_tout_resecable(
        contexte=ContexteClinique(
            atteinte_veine_splenique=True, localisation_tumeur="tete_crochet"
        )
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert any("à discuter en RCP" in a for a in resultat.alertes)


def test_alerte_rcp_systematique_des_que_non_resecable_pur():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True, circonference_ge_180=False)
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert any("réunion de concertation pluridisciplinaire" in a for a in resultat.alertes)


# ---------------------------------------------------------------------------
# Étape 3 — correction métastases / adénopathie à distance
# (intégrée dans evaluer_resecabilite_vasculaire, pas une fonction séparée)
# ---------------------------------------------------------------------------

def test_metastases_bascule_en_non_pertinent_meme_si_tout_resecable():
    data = _cas_tout_resecable(metastases=True)
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.NON_PERTINENT_METASTATIQUE
    # Le statut vasculaire pur reste consultable pour traçabilité :
    assert resultat.statut_vasculaire_avant_correction == StatutResecabilite.RESECABLE
    assert resultat.correction_appliquee is not None
    assert resultat.vaisseaux_determinants == []


def test_adenopathie_distance_force_localement_avance_meme_si_tout_resecable():
    data = _cas_tout_resecable(adenopathie_distance=True)
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE
    assert resultat.statut_vasculaire_avant_correction == StatutResecabilite.RESECABLE
    assert resultat.correction_appliquee is not None


def test_metastases_prime_sur_adenopathie_distance():
    """Reprend l'ordre du pseudocode source : SI metastases SINON SI adenopathie."""
    data = _cas_tout_resecable(metastases=True, adenopathie_distance=True)
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.NON_PERTINENT_METASTATIQUE


def test_sans_metastase_ni_adenopathie_distance_le_statut_vasculaire_est_inchange():
    data = _cas_tout_resecable(
        ams=ContactArterielSimple(contact_present=True, circonference_ge_180=True),  # LA
        metastases=False,
        adenopathie_distance=False,
    )
    resultat = evaluer_resecabilite_vasculaire(data)
    assert resultat.statut_global == StatutResecabilite.LOCALEMENT_AVANCE
    assert resultat.statut_vasculaire_avant_correction == StatutResecabilite.LOCALEMENT_AVANCE
    assert resultat.correction_appliquee is None


def test_adenopathie_distance_ajoute_une_alerte_de_correction():
    data = _cas_tout_resecable(adenopathie_distance=True)
    resultat = evaluer_resecabilite_vasculaire(data)
    assert any("Statut vasculaire modifié" in a for a in resultat.alertes)
