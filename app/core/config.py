from pydantic import ConfigDict

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=True)
    
    MONGO_URI: str = "mongodb://mongo:27017"
    DB_NAME: str = "metadata_db"
    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT: int = 10

settings = Settings()
