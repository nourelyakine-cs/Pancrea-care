from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.dossier import DossierPatient
from app.models.evaluation import (
    AnalyseMoleculaire,
    Biologie,
    EvaluationClinique,
    EvaluationComorbidite,
    HistologieBiologie,
    Imagerie,
    MetastaseLocalisation,
)
from app.schemas.evaluation import (
    AnalyseCreate,
    AnalyseUpdate,
    BiologieCreate,
    BiologieUpdate,
    ComorbiditeEvaluationCreate,
    ComorbiditeEvaluationUpdate,
    EvaluationCreate,
    EvaluationUpdate,
    HistologieCreate,
    HistologieUpdate,
    ImagerieCreate,
    ImagerieUpdate,
    MetastaseCreate,
    MetastaseUpdate,
)
from app.services.audit import log_action


# --- Évaluation clinique -----------------------------------------------------


def create_evaluation(
    db: Session,
    id_dossier: int,
    payload: EvaluationCreate,
    medecin_id: int | None = None,
) -> EvaluationClinique:
    dossier = db.get(DossierPatient, id_dossier)

    if dossier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable, impossible de créer l'évaluation.",
        )

    evaluation = EvaluationClinique(
        id_dossier=id_dossier,
        id_medecin_evaluateur=medecin_id,
        **payload.model_dump(),
    )

    db.add(evaluation)
    db.flush()

    log_action(
        db,
        medecin_id=medecin_id,
        action="evaluation_create",
        type_entite="evaluation_clinique",
        id_entite=evaluation.id_evaluation,
        detail=jsonable_encoder({
            "id_dossier": id_dossier,
            **payload.model_dump(),
        }),
    )

    db.commit()
    db.refresh(evaluation)

    return evaluation


def list_evaluations(
    db: Session,
    id_dossier: int,
) -> list[EvaluationClinique]:
    dossier = db.get(DossierPatient, id_dossier)

    if dossier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dossier {id_dossier} introuvable.",
        )

    return (
        db.query(EvaluationClinique)
        .filter(EvaluationClinique.id_dossier == id_dossier)
        .order_by(EvaluationClinique.date_evaluation.desc())
        .all()
    )


def get_evaluation(
    db: Session,
    id_evaluation: int,
) -> EvaluationClinique:
    evaluation = db.get(EvaluationClinique, id_evaluation)

    if evaluation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Évaluation {id_evaluation} introuvable.",
        )

    return evaluation


def update_evaluation(
    db: Session,
    id_evaluation: int,
    payload: EvaluationUpdate,
    medecin_id: int | None = None,
) -> EvaluationClinique:
    evaluation = get_evaluation(db, id_evaluation)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(evaluation, key, value)

    log_action(
        db,
        medecin_id=medecin_id,
        action="evaluation_update",
        type_entite="evaluation_clinique",
        id_entite=evaluation.id_evaluation,
        detail=jsonable_encoder(
            payload.model_dump(exclude_unset=True)
        ),
    )

    db.commit()
    db.refresh(evaluation)

    return evaluation


def delete_evaluation(
    db: Session,
    id_evaluation: int,
    medecin_id: int | None = None,
) -> None:
    evaluation = get_evaluation(db, id_evaluation)

    log_action(
        db,
        medecin_id=medecin_id,
        action="evaluation_delete",
        type_entite="evaluation_clinique",
        id_entite=evaluation.id_evaluation,
    )

    try:
        db.delete(evaluation)
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Impossible de supprimer cette évaluation : une décision y est "
                "rattachée (trace médico-légale). Elle ne peut être ni supprimée "
                "ni modifiée une fois une décision rendue."
            ),
        )


# --- Biologie (1:1) ----------------------------------------------------------


def get_biologie(
    db: Session,
    id_evaluation: int,
) -> Biologie:
    get_evaluation(db, id_evaluation)

    return (
        db.query(Biologie)
        .filter(Biologie.id_evaluation == id_evaluation)
        .first()
    )


def upsert_biologie(
    db: Session,
    id_evaluation: int,
    payload: BiologieCreate,
    medecin_id: int | None = None,
) -> Biologie:
    get_evaluation(db, id_evaluation)

    biologie = get_biologie(db, id_evaluation)

    if biologie is None:
        biologie = Biologie(
            id_evaluation=id_evaluation,
            **payload.model_dump(),
        )
        db.add(biologie)
        action = "biologie_create"

    else:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(biologie, key, value)

        action = "biologie_update"

    db.flush()

    log_action(
        db,
        medecin_id=medecin_id,
        action=action,
        type_entite="biologie",
        id_entite=biologie.id_biologie,
        detail=jsonable_encoder({
            "id_evaluation": id_evaluation,
            **payload.model_dump(),
        }),
    )

    db.commit()
    db.refresh(biologie)

    return biologie


def delete_biologie(
    db: Session,
    id_evaluation: int,
    medecin_id: int | None = None,
) -> None:
    get_evaluation(db, id_evaluation)

    biologie = get_biologie(db, id_evaluation)

    if biologie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune biologie pour l'évaluation {id_evaluation}.",
        )

    log_action(
        db,
        medecin_id=medecin_id,
        action="biologie_delete",
        type_entite="biologie",
        id_entite=biologie.id_biologie,
    )

    db.delete(biologie)
    db.commit()


# --- Histologie / biologie moléculaire (1:1) ----------------------------------


def get_histologie(
    db: Session,
    id_evaluation: int,
) -> HistologieBiologie:
    get_evaluation(db, id_evaluation)

    return (
        db.query(HistologieBiologie)
        .filter(HistologieBiologie.id_evaluation == id_evaluation)
        .first()
    )


def upsert_histologie(
    db: Session,
    id_evaluation: int,
    payload: HistologieCreate,
    medecin_id: int | None = None,
) -> HistologieBiologie:
    get_evaluation(db, id_evaluation)

    histologie = get_histologie(db, id_evaluation)

    if histologie is None:
        histologie = HistologieBiologie(
            id_evaluation=id_evaluation,
            **payload.model_dump(),
        )
        db.add(histologie)
        action = "histologie_create"

    else:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(histologie, key, value)

        action = "histologie_update"

    db.flush()

    log_action(
        db,
        medecin_id=medecin_id,
        action=action,
        type_entite="histologie_biologie",
        id_entite=histologie.id_histo,
        detail=jsonable_encoder({
            "id_evaluation": id_evaluation,
            **payload.model_dump(),
        }),
    )

    db.commit()
    db.refresh(histologie)

    return histologie


def delete_histologie(
    db: Session,
    id_evaluation: int,
    medecin_id: int | None = None,
) -> None:
    get_evaluation(db, id_evaluation)

    histologie = get_histologie(db, id_evaluation)

    if histologie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune histologie pour l'évaluation {id_evaluation}.",
        )

    log_action(
        db,
        medecin_id=medecin_id,
        action="histologie_delete",
        type_entite="histologie_biologie",
        id_entite=histologie.id_histo,
    )

    db.delete(histologie)
    db.commit()


# --- Imagerie (1:N) + métastases ---------------------------------------------


def list_imageries(
    db: Session,
    id_evaluation: int,
) -> list[Imagerie]:
    get_evaluation(db, id_evaluation)

    return (
        db.query(Imagerie)
        .filter(Imagerie.id_evaluation == id_evaluation)
        .order_by(Imagerie.date_imagerie.desc())
        .all()
    )


def create_imagerie(
    db: Session,
    id_evaluation: int,
    payload: ImagerieCreate,
    medecin_id: int | None = None,
) -> Imagerie:
    get_evaluation(db, id_evaluation)

    imagerie = Imagerie(
        id_evaluation=id_evaluation,
        **payload.model_dump(),
    )

    db.add(imagerie)
    db.flush()

    log_action(
        db,
        medecin_id=medecin_id,
        action="imagerie_create",
        type_entite="imagerie",
        id_entite=imagerie.id_imagerie,
        detail=jsonable_encoder({
            "id_evaluation": id_evaluation,
            **payload.model_dump(),
        }),
    )

    db.commit()
    db.refresh(imagerie)

    return imagerie


def get_imagerie(
    db: Session,
    id_imagerie: int,
) -> Imagerie:
    imagerie = db.get(Imagerie, id_imagerie)

    if imagerie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagerie {id_imagerie} introuvable.",
        )

    return imagerie


def update_imagerie(
    db: Session,
    id_imagerie: int,
    payload: ImagerieUpdate,
    medecin_id: int | None = None,
) -> Imagerie:
    imagerie = get_imagerie(db, id_imagerie)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(imagerie, key, value)

    log_action(
        db,
        medecin_id=medecin_id,
        action="imagerie_update",
        type_entite="imagerie",
        id_entite=imagerie.id_imagerie,
        detail=jsonable_encoder(
            payload.model_dump(exclude_unset=True)
        ),
    )

    db.commit()
    db.refresh(imagerie)

    return imagerie


def delete_imagerie(
    db: Session,
    id_imagerie: int,
    medecin_id: int | None = None,
) -> None:
    imagerie = get_imagerie(db, id_imagerie)

    log_action(
        db,
        medecin_id=medecin_id,
        action="imagerie_delete",
        type_entite="imagerie",
        id_entite=imagerie.id_imagerie,
    )

    db.delete(imagerie)
    db.commit()


def list_metastases(
    db: Session,
    id_imagerie: int,
) -> list[MetastaseLocalisation]:
    get_imagerie(db, id_imagerie)

    return (
        db.query(MetastaseLocalisation)
        .filter(MetastaseLocalisation.id_imagerie == id_imagerie)
        .all()
    )


def create_metastase(
    db: Session,
    id_imagerie: int,
    payload: MetastaseCreate,
    medecin_id: int | None = None,
) -> MetastaseLocalisation:
    get_imagerie(db, id_imagerie)

    metastase = MetastaseLocalisation(
        id_imagerie=id_imagerie,
        **payload.model_dump(),
    )

    db.add(metastase)

    try:
        db.flush()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Le site de métastase '{payload.site}' est déjà enregistré pour cette imagerie.",
        )

    log_action(
        db,
        medecin_id=medecin_id,
        action="metastase_create",
        type_entite="metastase_localisation",
        id_entite=metastase.id_metastase,
        detail=jsonable_encoder(
            payload.model_dump()
        ),
    )

    db.commit()
    db.refresh(metastase)

    return metastase


def get_metastase(
    db: Session,
    id_metastase: int,
) -> MetastaseLocalisation:
    metastase = db.get(MetastaseLocalisation, id_metastase)

    if metastase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Métastase {id_metastase} introuvable.",
        )

    return metastase


def update_metastase(
    db: Session,
    id_metastase: int,
    payload: MetastaseUpdate,
    medecin_id: int | None = None,
) -> MetastaseLocalisation:
    metastase = get_metastase(db, id_metastase)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(metastase, key, value)

    log_action(
        db,
        medecin_id=medecin_id,
        action="metastase_update",
        type_entite="metastase_localisation",
        id_entite=metastase.id_metastase,
        detail=jsonable_encoder(
            payload.model_dump(exclude_unset=True)
        ),
    )

    db.commit()
    db.refresh(metastase)

    return metastase


def delete_metastase(
    db: Session,
    id_metastase: int,
    medecin_id: int | None = None,
) -> None:
    metastase = get_metastase(db, id_metastase)

    log_action(
        db,
        medecin_id=medecin_id,
        action="metastase_delete",
        type_entite="metastase_localisation",
        id_entite=metastase.id_metastase,
    )

    db.delete(metastase)
    db.commit()


# --- Analyse moléculaire (1:N) -------------------------------------------------


def list_analyses(
    db: Session,
    id_evaluation: int,
) -> list[AnalyseMoleculaire]:
    get_evaluation(db, id_evaluation)

    return (
        db.query(AnalyseMoleculaire)
        .filter(AnalyseMoleculaire.id_evaluation == id_evaluation)
        .all()
    )


def create_analyse(
    db: Session,
    id_evaluation: int,
    payload: AnalyseCreate,
    medecin_id: int | None = None,
) -> AnalyseMoleculaire:
    get_evaluation(db, id_evaluation)

    analyse = AnalyseMoleculaire(
        id_evaluation=id_evaluation,
        **payload.model_dump(),
    )

    db.add(analyse)
    db.flush()

    log_action(
        db,
        medecin_id=medecin_id,
        action="analyse_moleculaire_create",
        type_entite="analyse_moleculaire",
        id_entite=analyse.id_analyse,
        detail=jsonable_encoder(
            payload.model_dump()
        ),
    )

    db.commit()
    db.refresh(analyse)

    return analyse


def get_analyse(
    db: Session,
    id_analyse: int,
) -> AnalyseMoleculaire:
    analyse = db.get(AnalyseMoleculaire, id_analyse)

    if analyse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analyse moléculaire {id_analyse} introuvable.",
        )

    return analyse


def update_analyse(
    db: Session,
    id_analyse: int,
    payload: AnalyseUpdate,
    medecin_id: int | None = None,
) -> AnalyseMoleculaire:
    analyse = get_analyse(db, id_analyse)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(analyse, key, value)

    log_action(
        db,
        medecin_id=medecin_id,
        action="analyse_moleculaire_update",
        type_entite="analyse_moleculaire",
        id_entite=analyse.id_analyse,
        detail=jsonable_encoder(
            payload.model_dump(exclude_unset=True)
        ),
    )

    db.commit()
    db.refresh(analyse)

    return analyse


def delete_analyse(
    db: Session,
    id_analyse: int,
    medecin_id: int | None = None,
) -> None:
    analyse = get_analyse(db, id_analyse)

    log_action(
        db,
        medecin_id=medecin_id,
        action="analyse_moleculaire_delete",
        type_entite="analyse_moleculaire",
        id_entite=analyse.id_analyse,
    )

    db.delete(analyse)
    db.commit()


# --- Comorbidité (liaison N:M) --------------------------------------------------


def list_comorbidites(
    db: Session,
    id_evaluation: int,
) -> list[EvaluationComorbidite]:
    get_evaluation(db, id_evaluation)

    return (
        db.query(EvaluationComorbidite)
        .filter(EvaluationComorbidite.id_evaluation == id_evaluation)
        .all()
    )


def add_comorbidite(
    db: Session,
    id_evaluation: int,
    payload: ComorbiditeEvaluationCreate,
    medecin_id: int | None = None,
) -> EvaluationComorbidite:
    get_evaluation(db, id_evaluation)

    link = EvaluationComorbidite(
        id_evaluation=id_evaluation,
        id_comorbidite=payload.id_comorbidite,
        severite=payload.severite,
        note=payload.note,
    )

    db.add(link)

    try:
        db.flush()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La comorbidité {payload.id_comorbidite} est déjà associée à cette évaluation.",
        )

    log_action(
        db,
        medecin_id=medecin_id,
        action="comorbidite_link_create",
        type_entite="evaluation_comorbidite",
        detail=jsonable_encoder({
            "id_evaluation": id_evaluation,
            **payload.model_dump(),
        }),
    )

    db.commit()
    db.refresh(link)

    return link


def update_comorbidite(
    db: Session,
    id_evaluation: int,
    id_comorbidite: int,
    payload: ComorbiditeEvaluationUpdate,
    medecin_id: int | None = None,
) -> EvaluationComorbidite:
    link = (
        db.query(EvaluationComorbidite)
        .filter(
            EvaluationComorbidite.id_evaluation == id_evaluation,
            EvaluationComorbidite.id_comorbidite == id_comorbidite,
        )
        .first()
    )

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comorbidité {id_comorbidite} non associée à l'évaluation {id_evaluation}.",
        )

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(link, key, value)

    db.commit()
    db.refresh(link)

    return link


def remove_comorbidite(
    db: Session,
    id_evaluation: int,
    id_comorbidite: int,
    medecin_id: int | None = None,
) -> None:
    link = (
        db.query(EvaluationComorbidite)
        .filter(
            EvaluationComorbidite.id_evaluation == id_evaluation,
            EvaluationComorbidite.id_comorbidite == id_comorbidite,
        )
        .first()
    )

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comorbidité {id_comorbidite} non associée à l'évaluation {id_evaluation}.",
        )

    db.delete(link)
    db.commit()