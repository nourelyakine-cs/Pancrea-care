from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
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
from app.models import donnees_derivees, compte  # noqa: F401  (import pour create_all)
from app.routes import (
    auth,
    admin as admin_router,
    dossier as dossier_router,
    patient,
    clinical_rules as clinical_rules_router,
)

# Le schéma est géré par Supabase via backend/database/*.sql et ses migrations.
# Ne pas exécuter create_all() à l'import : cela rendrait /health et /docs
# indisponibles dès qu'une URL DATABASE_URL est temporairement inaccessible.

app = FastAPI(title=settings.APP_NAME, environment=settings.ENVIRONMENT)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=(
        r".*" if settings.ENVIRONMENT == "development" else r"https?://(localhost|127\.0\.0\.1)(:\d+)?$"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin_router.router)
app.include_router(patient.router)
app.include_router(dossier_router.router)
app.include_router(clinical_rules_router.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}