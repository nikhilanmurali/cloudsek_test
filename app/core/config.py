from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://mongo:27017"
    DB_NAME: str = "metadata_db"
    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
