import enum
from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.dossier import DossierPatient
from app.models.evaluation import (
    Biologie,
    EvaluationClinique,
    EvaluationComorbidite,
    HistologieBiologie,
    Imagerie,
    MetastaseLocalisation,
)
from app.models.patient import Patient
from app.models.parcours_therapeutique import EvaluationParcoursTherapeutique
from app.models.reference import Comorbidite
from app.models.traitement import Traitement
from app.schemas.patient import PatientCreate, PatientUpdate
from app.schemas.patient_detail import PatientDetailRead
from app.services.audit import log_action


def create_patient(
    db: Session,
    payload: PatientCreate,
    medecin_id: int | None = None,
) -> Patient:
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.flush()
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_create",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail=payload.model_dump(),
    )
    db.commit()
    db.refresh(patient)
    return patient


def list_patients(
    db: Session,
    nom: str | None = None,
    sexe: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Patient]:
    query = db.query(Patient)
    if nom:
        query = query.filter(Patient.nom.ilike(f"%{nom}%"))
    if sexe:
        query = query.filter(Patient.sexe == sexe)
    patients = query.offset(skip).limit(limit).all()
    _attach_dernier_bilan(db, patients)
    return patients


def _attach_dernier_bilan(db: Session, patients: list[Patient]) -> None:
    """Attache à chaque patient son dossier, sa dernière évaluation et le
    dernier bilan calculé (stade global + catégories TNM)."""
    patient_ids = [p.id_patient for p in patients]
    if not patient_ids:
        return

    dossiers = (
        db.query(DossierPatient)
        .filter(DossierPatient.id_patient.in_(patient_ids))
        .order_by(DossierPatient.id_dossier.asc())
        .all()
    )
    if not dossiers:
        return

    evaluations = (
        db.query(EvaluationClinique)
        .filter(
            EvaluationClinique.id_dossier.in_(
                [d.id_dossier for d in dossiers]
            )
        )
        .order_by(
            EvaluationClinique.date_evaluation.desc(),
            EvaluationClinique.id_evaluation.desc(),
        )
        .all()
    )

    derniere_eval: dict[int, EvaluationClinique] = {}
    for evaluation in evaluations:
        derniere_eval.setdefault(evaluation.id_dossier, evaluation)

    derniers_derivees: dict[int, DonneesDerivees] = {}
    if evaluations:
        derivees = (
            db.query(DonneesDerivees)
            .filter(
                DonneesDerivees.id_evaluation.in_(
                    [e.id_evaluation for e in evaluations]
                )
            )
            .all()
        )
        for derivee in derivees:
            courant = derniers_derivees.get(derivee.id_evaluation)
            if courant is None or derivee.date_calcul > courant.date_calcul:
                derniers_derivees[derivee.id_evaluation] = derivee

    dossier_par_patient: dict[int, DossierPatient] = {}
    for dossier in dossiers:
        dossier_par_patient.setdefault(dossier.id_patient, dossier)

    for patient in patients:
        dossier = dossier_par_patient.get(patient.id_patient)
        if dossier is None:
            continue
        evaluation = derniere_eval.get(dossier.id_dossier)
        derivee = (
            derniers_derivees.get(evaluation.id_evaluation)
            if evaluation
            else None
        )
        patient.id_dossier = dossier.id_dossier
        patient.id_evaluation = (
            evaluation.id_evaluation if evaluation else None
        )
        patient.date_derniere_evaluation = (
            evaluation.date_evaluation if evaluation else None
        )
        patient.stade_global = derivee.stade_global if derivee else None
        patient.resecabilite = derivee.resecabilite if derivee else None
        patient.categorie_t = derivee.categorie_t if derivee else None
        patient.categorie_n = derivee.categorie_n if derivee else None
        patient.categorie_m = derivee.categorie_m if derivee else None


def get_patient(db: Session, id_patient: int) -> Patient:
    patient = db.get(Patient, id_patient)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


# --- Fiche détaillée ("Voir Détails") ---------------------------------------


def _to_float(value: Decimal | float | int | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _to_str(value: enum.Enum | str | None) -> str | None:
    """Normalise une valeur d'enum SQLAlchemy (Python ou PostgreSQL) en chaîne."""
    if value is None:
        return None
    if isinstance(value, enum.Enum):
        return str(value.value)
    return str(value)


def _age(date_naissance: date | None) -> int | None:
    if date_naissance is None:
        return None
    today = date.today()
    value = today.year - date_naissance.year
    if (today.month, today.day) < (date_naissance.month, date_naissance.day):
        value -= 1
    return value if value >= 0 else None


def _duree_mois(debut: date | None, fin: date | None) -> float | None:
    if debut is None:
        return None
    end = fin or date.today()
    if end < debut:
        return None
    return round((end - debut).days / 30.4375, 2)


def _biologie_detail(db: Session, id_evaluation: int) -> dict:
    biologie = (
        db.query(Biologie).filter(Biologie.id_evaluation == id_evaluation).first()
    )
    if biologie is None:
        return {}
    return {
        "ca19_9": _to_float(biologie.ca19_9),
        "ca19_9_multiple_lsn": _to_float(biologie.ca19_9_multiple_lsn),
        "bilirubine": _to_float(biologie.bilirubine),
        "bilirubine_ratio_lsn": _to_float(biologie.bilirubine_ratio_lsn),
        "statut_dpd": _to_str(biologie.statut_dpd),
        "albuminemie": _to_float(biologie.albuminemie),
        "cholestase": biologie.cholestase,
    }


def _imagerie_detail(db: Session, id_evaluation: int) -> dict:
    imagerie = (
        db.query(Imagerie)
        .filter(Imagerie.id_evaluation == id_evaluation)
        .order_by(Imagerie.date_imagerie.desc(), Imagerie.id_imagerie.desc())
        .first()
    )
    if imagerie is None:
        return {}
    sites = (
        db.query(MetastaseLocalisation)
        .filter(MetastaseLocalisation.id_imagerie == imagerie.id_imagerie)
        .order_by(MetastaseLocalisation.id_metastase.asc())
        .all()
    )
    return {
        "id_imagerie": imagerie.id_imagerie,
        "type_imagerie": _to_str(imagerie.type_imagerie),
        "date_imagerie": imagerie.date_imagerie,
        "localisation_tumorale": _to_str(imagerie.localisation_tumorale),
        "taille_tumorale_cm": _to_float(imagerie.taille_tumorale_cm),
        "contact_ams": _to_str(imagerie.contact_ams),
        "contact_tronc_coeliaque": _to_str(imagerie.contact_tronc_coeliaque),
        "contact_art_hepatique": _to_str(imagerie.contact_art_hepatique),
        "contact_vms_vp": _to_str(imagerie.contact_vms_vp),
        "extension_ganglionnaire_regionale": imagerie.extension_ganglionnaire_regionale,
        "extension_ganglionnaire_distance": imagerie.extension_ganglionnaire_distance,
        "metastases_presentes": imagerie.metastases_presentes,
        "sites_metastases": [_to_str(site.site) for site in sites],
    }


def _histologie_detail(db: Session, id_evaluation: int) -> dict:
    histologie = (
        db.query(HistologieBiologie)
        .filter(HistologieBiologie.id_evaluation == id_evaluation)
        .first()
    )
    if histologie is None:
        return {}
    return {
        "preuve_histologique": histologie.preuve_histologique,
        "statut_brca_germinal": _to_str(histologie.statut_brca_germinal),
        "statut_kras": _to_str(histologie.statut_kras),
        "statut_msi_dmmr": _to_str(histologie.statut_msi_dmmr),
        "fusion_ntrk": _to_str(histologie.fusion_ntrk),
        "fusion_nrg1": _to_str(histologie.fusion_nrg1),
    }


def _comorbidites_detail(db: Session, id_evaluation: int) -> dict:
    liens = (
        db.query(EvaluationComorbidite)
        .filter(EvaluationComorbidite.id_evaluation == id_evaluation)
        .order_by(EvaluationComorbidite.id_comorbidite.asc())
        .all()
    )
    if not liens:
        return {}

    comorbidites = (
        db.query(Comorbidite)
        .filter(Comorbidite.id_comorbidite.in_([l.id_comorbidite for l in liens]))
        .all()
    )
    libelles = {
        c.id_comorbidite: (c.libelle_fr or c.code) for c in comorbidites
    }

    libelles_liste: list[str] = []
    lourdes = False
    for lien in liens:
        majeure = _to_str(lien.severite) == "majeure"
        lourdes = lourdes or majeure
        libelle = libelles.get(lien.id_comorbidite)
        if libelle is None:
            libelle = f"Comorbidité #{lien.id_comorbidite}"
        libelles_liste.append(f"{libelle} (majeure)" if majeure else libelle)

    return {
        "comorbidites_lourdes": lourdes,
        "comorbidites": libelles_liste,
    }


def _parcours_evaluation_detail(db: Session, id_evaluation: int) -> dict:
    parcours = (
        db.query(EvaluationParcoursTherapeutique)
        .filter(EvaluationParcoursTherapeutique.id_evaluation == id_evaluation)
        .order_by(
            EvaluationParcoursTherapeutique.date_reevaluation.desc().nullslast(),
            EvaluationParcoursTherapeutique.id_parcours.desc(),
        )
        .first()
    )
    if parcours is None:
        return {}
    return {
        "angiocholite": parcours.angiocholite,
        "tumeur_controlee": parcours.tumeur_controlee,
        "nouvelles_metastases": parcours.nouvelles_metastases,
        "chirurgie_d_emblee": parcours.chirurgie_d_emblee,
        "traitement_medical_prevu": parcours.traitement_medical_prevu,
        "pas_de_progression_apres_16_semaines_platine": (
            parcours.pas_de_progression_apres_16_semaines_platine
        ),
    }


def _bilan_derivees(db: Session, id_evaluation: int) -> dict:
    donnees = (
        db.query(DonneesDerivees)
        .filter(DonneesDerivees.id_evaluation == id_evaluation)
        .order_by(DonneesDerivees.date_calcul.desc())
        .all()
    )
    if not donnees:
        return {}
    derivee = donnees[0]
    return {
        "categorie_t": _to_str(derivee.categorie_t),
        "categorie_n": _to_str(derivee.categorie_n),
        "categorie_m": _to_str(derivee.categorie_m),
        "stade_global": _to_str(derivee.stade_global),
        "resecabilite": _to_str(derivee.resecabilite),
        "critere_abc_a": derivee.critere_abc_a,
        "critere_abc_b": derivee.critere_abc_b,
        "critere_abc_c": derivee.critere_abc_c,
        "sous_categorie_abc": derivee.sous_categorie_abc,
        "date_calcul": derivee.date_calcul,
    }


def _libelle_ligne(traitement: Traitement) -> str:
    protocole = traitement.protocole
    libelle = (protocole.libelle_fr or protocole.code) if protocole else None
    if traitement.numero_ligne is not None:
        return f"L{traitement.numero_ligne} · {libelle}" if libelle else f"L{traitement.numero_ligne}"
    return libelle or f"Traitement #{traitement.id_traitement}"


def _protocole_code(traitement: Traitement | None) -> str | None:
    if traitement is None or traitement.protocole is None:
        return None
    return traitement.protocole.code


def _parcours_traitements_detail(traitements: list[Traitement]) -> dict:
    if not traitements:
        return {}

    lignes = [t for t in traitements if t.numero_ligne is not None]
    courante = max(lignes, key=lambda t: t.numero_ligne) if lignes else None
    precedente = None
    if courante is not None:
        precedente = next(
            (
                t
                for t in reversed(lignes)
                if t.numero_ligne is not None
                and t.numero_ligne < courante.numero_ligne
            ),
            None,
        )

    notes = [t.notes for t in traitements if t.notes]

    return {
        "ligne_traitement_actuelle": courante.numero_ligne if courante else None,
        "reponse_traitement_en_cours": _to_str(courante.reponse) if courante else None,
        "traitements_recus": [_libelle_ligne(t) for t in traitements],
        "traitements_recus_texte": " | ".join(notes) if notes else None,
        "ligne_precedente": _protocole_code(precedente),
        "duree_chimiotherapie_mois": _duree_mois(
            courante.date_debut if courante else None,
            courante.date_fin if courante else None,
        ),
        "toxicite_residuelle": courante.toxicite_residuelle if courante else None,
        "details_toxicite": courante.type_toxicite if courante else None,
    }


def get_patient_detail(db: Session, id_patient: int) -> PatientDetailRead:
    """Fiche complète d'un patient pour l'écran « Voir Détails ».

    Agrège en un seul payload l'identité, la dernière évaluation (clinique,
    biologie, imagerie, histologie, comorbidités, parcours thérapeutique) et
    le dernier bilan CDSS. Un patient sans dossier ou sans évaluation renvoie
    malgré tout ses données d'identité, les autres champs restant `None`.
    """
    patient = get_patient(db, id_patient)

    dossier = (
        db.query(DossierPatient)
        .filter(DossierPatient.id_patient == id_patient)
        .order_by(DossierPatient.id_dossier.asc())
        .first()
    )

    detail: dict = {
        "id_patient": patient.id_patient,
        "nom": patient.nom,
        "prenom": patient.prenom,
        "date_naissance": patient.date_naissance,
        "age": _age(patient.date_naissance),
        "sexe": _to_str(patient.sexe),
        "telephone": patient.telephone,
        "email": patient.email,
        "adresse": patient.adresse,
    }

    if dossier is None:
        return PatientDetailRead(**detail)

    detail["id_dossier"] = dossier.id_dossier
    detail["statut_dossier"] = _to_str(dossier.statut)

    traitements = (
        db.query(Traitement)
        .filter(Traitement.id_dossier == dossier.id_dossier)
        .order_by(
            Traitement.numero_ligne.asc(),
            Traitement.date_debut.asc(),
            Traitement.id_traitement.asc(),
        )
        .all()
    )
    detail.update(_parcours_traitements_detail(traitements))

    evaluation = (
        db.query(EvaluationClinique)
        .filter(EvaluationClinique.id_dossier == dossier.id_dossier)
        .order_by(
            EvaluationClinique.date_evaluation.desc(),
            EvaluationClinique.id_evaluation.desc(),
        )
        .first()
    )
    if evaluation is None:
        return PatientDetailRead(**detail)

    id_evaluation = evaluation.id_evaluation
    detail.update(
        {
            "id_evaluation": id_evaluation,
            "date_derniere_evaluation": evaluation.date_evaluation,
            "contexte": _to_str(evaluation.contexte),
            "ecog": evaluation.ecog,
            "etat_nutritionnel": _to_str(evaluation.etat_nutritionnel),
            "douleur_presente": evaluation.douleur_presente,
            "intensite_douleur": evaluation.intensite_douleur,
            "ictere": evaluation.ictere,
            "diabete": _to_str(evaluation.diabete),
        }
    )
    detail.update(_biologie_detail(db, id_evaluation))
    detail.update(_imagerie_detail(db, id_evaluation))
    detail.update(_histologie_detail(db, id_evaluation))
    detail.update(_comorbidites_detail(db, id_evaluation))
    detail.update(_parcours_evaluation_detail(db, id_evaluation))
    detail.update(_bilan_derivees(db, id_evaluation))

    return PatientDetailRead(**detail)


def update_patient(
    db: Session,
    id_patient: int,
    payload: PatientUpdate,
    medecin_id: int | None = None,
) -> Patient:
    patient = get_patient(db, id_patient)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_update",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(
    db: Session,
    id_patient: int,
    medecin_id: int | None = None,
) -> None:
    patient = get_patient(db, id_patient)
    log_action(
        db,
        medecin_id=medecin_id,
        action="patient_delete",
        type_entite="patient",
        id_entite=patient.id_patient,
        detail={"nom": patient.nom, "prenom": patient.prenom},
    )
    try:
        db.delete(patient)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Impossible de supprimer ce patient : un dossier clinique lui est "
                "associé. Pour respecter la traçabilité médico-légale, clôturez ou "
                "archivez le dossier (statut 'clos'/'archive') au lieu de supprimer "
                "le patient."
            ),
        )
