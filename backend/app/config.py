from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENVIRONMENT: str = "development"
    APP_NAME: str = "PANCRA"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    FRONTEND_URL: str = "http://localhost:3000"
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30

    RESEND_API_KEY: str | None = None
    RESEND_FROM: str = "PANCRA <onboarding@resend.dev>"


settings = Settings()
