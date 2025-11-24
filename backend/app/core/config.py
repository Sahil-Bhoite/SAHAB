import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SAHAB API"
    API_V1_STR: str = "/api/v1"
    GOOGLE_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
