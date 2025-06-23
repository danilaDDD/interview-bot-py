import os
from datetime import datetime
from pathlib import Path

import pytz
from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)

def get_env_file_path() -> str:
    path = f"{BASE_DIR}/env/.env.{os.getenv('ENV', 'dev')}"
    if not os.path.exists(path):
        return f"{BASE_DIR}/env/.env"
    return path

class Settings(BaseSettings):
    ENV: str = "dev"
    BOT_TOKEN: str
    DB_DRIVER_PREFIX: str = "mysql+pymysql"
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str
    DB_NAME: str
    TEST_API_ID: str = ''
    TEST_API_HASH: str = ''

    def get_database_url(self) -> str:
        return f"{self.DB_DRIVER_PREFIX}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_env_file_path(self) -> str:
        return self.e

    model_config = SettingsConfigDict(
        env_file_encoding = 'utf-8',
    )

def load_settings() -> Settings:
    env_vars = dotenv_values(f"{BASE_DIR}/env/.env.{os.getenv('ENV', 'dev')}")
    return Settings(_env_file=get_env_file_path(), **env_vars)

TZ = pytz.timezone("Europe/Moscow")
now_with_tz = lambda: datetime.now(TZ)