from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    APP_NAME: str = "PANCRA"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    # Mode développement : quand True, les routes protégées sont accessibles
    # SANS vérification du jeton JWT (utilise un médecin « démo »).
    # À garder à False en production.
    DISABLE_AUTH: bool = False

    # URL du frontend, utilisée comme redirect_to pour les liens de
    # réinitialisation de mot de passe envoyés par Supabase.
    FRONTEND_URL: str = "http://localhost:3000"


settings = Settings()
