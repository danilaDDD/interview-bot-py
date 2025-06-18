import os
from datetime import datetime
from pathlib import Path

import pytz
from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "dev"
    BOT_TOKEN: str
    DB_DRIVER_PREFIX: str = "mysql+pymysql"
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str
    DB_NAME: str

    def get_database_url(self) -> str:
        return f"{self.DB_DRIVER_PREFIX}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file = f"env/.env.{os.getenv('ENV', 'dev')}",
        env_file_encoding = 'utf-8',
    )

BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)

def load_settings() -> Settings:
    env_vars = dotenv_values(f"{BASE_DIR}/env/.env.{os.getenv('ENV', 'dev')}")
    return Settings(**env_vars)

TZ = pytz.timezone("Europe/Moscow")
now_with_tz = lambda: datetime.now(TZ)