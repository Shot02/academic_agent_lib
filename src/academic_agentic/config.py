from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    tool_gateway_url: str | None = None
    tool_gateway_token: str | None = None
    memory_window: int = 16
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()