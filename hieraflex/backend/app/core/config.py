from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HieraFlex"
    app_env: str = "dev"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    replay_speed: float = 60.0
    enable_pv: bool = True
    enable_battery: bool = True
    enable_ev: bool = True

    hf_token: str | None = None
    hf_dataset_repo_id: str | None = None
    hf_model_repo_id: str | None = None
    hf_space_repo_id: str | None = None
    hf_username: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
