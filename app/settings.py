from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: list[str]
    database_url: str
    smtp_server: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = "test@example.com"
    smtp_password: str = "test"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
