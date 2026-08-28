from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    APP_NAME: str = "PANCRA"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str


settings = Settings()
