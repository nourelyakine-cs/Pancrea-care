from sqlalchemy.orm import Session

from app.models.donnees_derivees import DonneesDerivees
from app.models.dossier import DossierPatient
from app.models.evaluation import EvaluationClinique
from app.services import acces


def list_patient_evaluations(
    db: Session,
    id_patient: int,
    medecin_id: int | None = None,
) -> list[dict]:
    """Liste toutes les évaluations d'un patient (quel que soit son dossier),
    enrichies du médecin évaluateur et du dernier DonneesDerivees calculé."""
    acces.exiger_patient(db, id_patient, medecin_id)

    dossiers = (
        db.query(DossierPatient)
        .filter(DossierPatient.id_patient == id_patient)
        .all()
    )

    if not dossiers:
        return []

    dossier_ids = [dossier.id_dossier for dossier in dossiers]

    evaluations = (
        db.query(EvaluationClinique)
        .filter(EvaluationClinique.id_dossier.in_(dossier_ids))
        .order_by(
            EvaluationClinique.date_evaluation.desc(),
            EvaluationClinique.id_evaluation.desc(),
        )
        .all()
    )

    eval_ids = [evaluation.id_evaluation for evaluation in evaluations]

    donnees = (
        db.query(DonneesDerivees)
        .filter(DonneesDerivees.id_evaluation.in_(eval_ids))
        .all()
        if eval_ids
        else []
    )

    dernieres: dict[int, DonneesDerivees] = {}
    for donnee in donnees:
        courante = dernieres.get(donnee.id_evaluation)
        if courante is None or donnee.date_calcul > courante.date_calcul:
            dernieres[donnee.id_evaluation] = donnee

    result: list[dict] = []
    for evaluation in evaluations:
        medecin = evaluation.medecin_evaluateur
        donnee = dernieres.get(evaluation.id_evaluation)

        result.append({
            "id_evaluation": evaluation.id_evaluation,
            "id_dossier": evaluation.id_dossier,
            "date_evaluation": evaluation.date_evaluation,
            "contexte": evaluation.contexte,
            "ecog": evaluation.ecog,
            "etat_nutritionnel": evaluation.etat_nutritionnel,
            "douleur_presente": evaluation.douleur_presente,
            "ictere": evaluation.ictere,
            "date_creation": evaluation.date_creation,
            "medecin_nom": medecin.nom if medecin else None,
            "medecin_prenom": medecin.prenom if medecin else None,
            "stade_global": donnee.stade_global if donnee else None,
            "resecabilite": donnee.resecabilite if donnee else None,
            "categorie_t": donnee.categorie_t if donnee else None,
            "categorie_n": donnee.categorie_n if donnee else None,
            "categorie_m": donnee.categorie_m if donnee else None,
            "sous_categorie_abc": donnee.sous_categorie_abc if donnee else None,
            "date_calcul": donnee.date_calcul if donnee else None,
        })

    return result
