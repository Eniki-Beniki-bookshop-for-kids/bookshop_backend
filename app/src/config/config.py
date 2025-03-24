import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Завантажуємо змінні середовища
load_dotenv()


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    secret_key: str
    algorithm: str

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # mail_username: str
    # mail_password: str
    # mail_from: str
    # mail_port: int
    # mail_server: str
    # redis_host: str = "localhost"
    # redis_port: int = 6379

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
