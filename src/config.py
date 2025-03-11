import os
from pydantic import BaseSettings


# Load environment variables from .env file
# This is a simple way to load environment variables from a file
# and use them in the application.  The .env file should be in the
# root of the project.
class Settings(BaseSettings):
    google_service_json_file: str
    port: int
    host: str
    timeout_keepalive: int
    http_lib: str
    reload: bool

    class Config:
        env_file = ".env"


settings = Settings()
