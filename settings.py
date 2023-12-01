from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr = Field(default=...)
    api_host: str = Field(default=...)
    api_key: str = Field(default=...)
    py_env: str = Field(default="PRODUCTION")
    database: str = Field(default="database.db")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


config = Settings()
