from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
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
from app.schemas.full_patient import FullPatientCreate
from app.services.audit import log_action


def create_full_patient(
    db: Session,
    payload: FullPatientCreate,
    medecin_id: int | None = None,
) -> dict:
    """Crée en une seule transaction : patient + dossier + première évaluation
    (et toutes ses données) + une décision (recommandation à générer)."""
    patient = Patient(
        nom=payload.nom,
        prenom=payload.prenom,
        date_naissance=payload.date_naissance,
        sexe=payload.sexe,
        telephone=payload.telephone,
        email=payload.email,
        adresse=payload.adresse,
    )
    db.add(patient)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de créer le patient (données invalides ou en conflit).",
        )
    log_action(
        db, medecin_id, "patient_create", "patient", patient.id_patient,
        {"nom": payload.nom, "prenom": payload.prenom, "email": payload.email},
    )

    dossier = DossierPatient(id_patient=patient.id_patient, id_medecin_referent=medecin_id)
    db.add(dossier)
    db.flush()
    log_action(
        db, medecin_id, "dossier_create", "dossier_patient", dossier.id_dossier,
        {"id_patient": patient.id_patient},
    )

    for ant in payload.antecedents:
        antecedent = AntecedentFamilial(id_dossier=dossier.id_dossier, **ant.model_dump())
        db.add(antecedent)
    for mut in payload.mutations:
        mutation = MutationGerminale(id_dossier=dossier.id_dossier, **mut.model_dump())
        db.add(mutation)

    ev = payload.evaluation
    evaluation = EvaluationClinique(
        id_dossier=dossier.id_dossier,
        id_medecin_evaluateur=medecin_id,
        **ev.model_dump(
            exclude={"biologie", "imageries", "histologie", "analyses", "comorbidites"}
        ),
    )
    db.add(evaluation)
    db.flush()
    id_evaluation = evaluation.id_evaluation
    log_action(
        db, medecin_id, "evaluation_create", "evaluation_clinique", id_evaluation,
        {"id_dossier": dossier.id_dossier},
    )

    if ev.biologie is not None:
        db.add(Biologie(id_evaluation=id_evaluation, **ev.biologie.model_dump()))
    if ev.histologie is not None:
        db.add(HistologieBiologie(id_evaluation=id_evaluation, **ev.histologie.model_dump()))

    for img in ev.imageries:
        metas = img.metastases
        img_data = img.model_dump(exclude={"metastases"})
        imagerie = Imagerie(id_evaluation=id_evaluation, **img_data)
        db.add(imagerie)
        db.flush()
        for meta in metas:
            db.add(MetastaseLocalisation(id_imagerie=imagerie.id_imagerie, **meta.model_dump()))

    for analyse in ev.analyses:
        db.add(AnalyseMoleculaire(id_evaluation=id_evaluation, **analyse.model_dump()))

    for comorb in ev.comorbidites:
        db.add(
            EvaluationComorbidite(
                id_evaluation=id_evaluation,
                id_comorbidite=comorb.id_comorbidite,
                severite=comorb.severite,
                note=comorb.note,
            )
        )

    decision = Decision(
        id_evaluation=id_evaluation,
        decide_par=medecin_id,
        snapshot_patient=None,
        resume="Décision créée.",
        decision_medecin=None,
        necessite_rcp=False,
    )
    db.add(decision)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de créer la décision (conflit de traçabilité).",
        )
    log_action(
        db, medecin_id, "decision_create", "decision", decision.id_decision,
        {"id_evaluation": id_evaluation},
    )

    db.commit()

    return {
        "id_patient": patient.id_patient,
        "id_dossier": dossier.id_dossier,
        "id_evaluation": id_evaluation,
        "id_decision": decision.id_decision,
        "date_creation": evaluation.date_creation,
    }
