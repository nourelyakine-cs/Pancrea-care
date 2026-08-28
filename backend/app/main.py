from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import auth, patient

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

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
