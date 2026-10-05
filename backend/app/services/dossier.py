from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.decision import Decision
from app.models.dossier import AntecedentFamilial, DossierPatient, MutationGerminale
from app.models.evaluation import (
    AnalyseMoleculaire,
    Biologie,
    EvaluationClinique,
    EvaluationComorbidite,
    HistologieBiologie,
    Imagerie,
    MetastaseLocalisation,
)
from app.models.patient import Patient
from app.models.traitement import Traitement
from app.schemas.dossier_detail import DossierDetailRead
from app.services import acces


def get_dossier(
    db: Session,
    id_dossier: int,
    medecin_id: int | None = None,
) -> DossierPatient:
    """Dossier par son id, s'il est accessible au médecin connecté."""
    return acces.exiger_dossier(db, id_dossier, medecin_id)


# --- Détail complet du dossier (patient + évaluations + décisions + traitements) ----

def get_dossier_detail(
    db: Session,
    id_dossier: int,
    medecin_id: int | None = None,
) -> DossierDetailRead:
    """Assemble le dossier complet : patient, antécédents, mutations, évaluations
    (avec toutes leurs données) + décisions + traitements."""
    dossier = get_dossier(db, id_dossier, medecin_id)

    patient = db.get(Patient, dossier.id_patient)
    antecedents = (
        db.query(AntecedentFamilial)
        .filter(AntecedentFamilial.id_dossier == id_dossier)
        .all()
    )
    mutations = (
        db.query(MutationGerminale)
        .filter(MutationGerminale.id_dossier == id_dossier)
        .all()
    )
    evaluations = (
        db.query(EvaluationClinique)
        .filter(EvaluationClinique.id_dossier == id_dossier)
        .order_by(EvaluationClinique.date_evaluation.desc())
        .all()
    )
    traitements = (
        db.query(Traitement)
        .filter(Traitement.id_dossier == id_dossier)
        .order_by(Traitement.numero_ligne.asc())
        .all()
    )

    detail_evaluations = []
    for ev in evaluations:
        id_ev = ev.id_evaluation
        biologie = (
            db.query(Biologie).filter(Biologie.id_evaluation == id_ev).first()
        )
        histologie = (
            db.query(HistologieBiologie).filter(HistologieBiologie.id_evaluation == id_ev).first()
        )
        imageries = (
            db.query(Imagerie).filter(Imagerie.id_evaluation == id_ev).all()
        )
        analyses = (
            db.query(AnalyseMoleculaire).filter(AnalyseMoleculaire.id_evaluation == id_ev).all()
        )
        comorbidites = (
            db.query(EvaluationComorbidite).filter(EvaluationComorbidite.id_evaluation == id_ev).all()
        )
        decisions = (
            db.query(Decision)
            .filter(Decision.id_evaluation == id_ev)
            .order_by(Decision.date_decision.desc())
            .all()
        )

        detail_imageries = []
        for img in imageries:
            metastases = (
                db.query(MetastaseLocalisation)
                .filter(MetastaseLocalisation.id_imagerie == img.id_imagerie)
                .all()
            )
            detail_imageries.append(
                {
                    **img.__dict__,
                    "metastases": metastases,
                }
            )

        detail_evaluations.append(
            {
                **ev.__dict__,
                "biologie": biologie,
                "histologie": histologie,
                "imageries": detail_imageries,
                "analyses": analyses,
                "comorbidites": comorbidites,
                "decisions": decisions,
            }
        )

    return DossierDetailRead(
        id_dossier=dossier.id_dossier,
        statut=dossier.statut,
        date_creation=dossier.date_creation,
        date_modification=dossier.date_modification,
        patient=patient,
        antecedents=antecedents,
        mutations=mutations,
        evaluations=detail_evaluations,
        traitements=traitements,
    )
