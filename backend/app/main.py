from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import (
    medecin,
    patient,
    audit,
    dossier,
    reference,
    evaluation,
    traitement,
    decision,
)  # noqa: F401  (import pour create_all)
from app.routes import (
    auth,
    audit as audit_router,
    decision as decision_router,
    dossier as dossier_router,
    evaluation as evaluation_router,
    medecin as medecin_router,
    patient,
    reference as reference_router,
    traitement as traitement_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, environment=settings.ENVIRONMENT)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(medecin_router.router)
app.include_router(audit_router.router)
app.include_router(dossier_router.router)
app.include_router(evaluation_router.router)
app.include_router(traitement_router.router)
app.include_router(reference_router.router)
app.include_router(decision_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
