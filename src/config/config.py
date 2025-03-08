from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    secret_key: str
    algorithm: str
    # mail_username: str
    # mail_password: str
    # mail_from: str
    # mail_port: int
    # mail_server: str
    # redis_host: str = "localhost"
    # redis_port: int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
