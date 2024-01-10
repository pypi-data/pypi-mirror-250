import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class FastAPIConfig(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG")
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    ORIGINS: list = [
        "http://localhost",
        "http://localhost:8000",
        "http://0.0.0.0:8000",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "app_"
        case_sensitive = True


class HunterConfig(BaseSettings):
    API_KEY: str = os.getenv("API_KEY")
    BASE_URL: str = "https://api.hunter.io/v2"
    HEADERS: dict = {"Content-Type": "application/json"}


app_settings = FastAPIConfig()
hunter_settings = HunterConfig()
