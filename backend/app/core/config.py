from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./club_mziya.db"
    PROJECT_NAME: str = "Club Mziya API"


settings = Settings()
