import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    google_service_json_file: str
    backend_port: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()
