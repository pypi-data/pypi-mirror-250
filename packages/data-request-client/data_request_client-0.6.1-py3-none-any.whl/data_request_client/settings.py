import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str = "https://data-requests.caltech.modelyst.com"
    API_KEY: SecretStr = "secret"

    # Config
    model_config = SettingsConfigDict(
        env_file=os.environ.get("DATA_REQUEST_CONFIG_FILE", ".env")
    )


settings = Settings()
