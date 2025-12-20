from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    DEBUG: bool

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    COOKIE_NAME: str
    COOKIE_SECURE: bool
    COOKIE_HTTPONLY: bool
    COOKIE_SAMESITE: str

    DATABASE_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    AUDIT_TIMEOUT_SECONDS: int
    MAX_AUDIT_RETRIES: int

    class Config:
        env_file = ".env"

settings = Settings()
