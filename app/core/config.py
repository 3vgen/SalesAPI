from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    # удобно собрать URL
    # @property
    # def REDIS_URL(self) -> str:
    #     return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    #
    # --- настройки загрузки ---
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

# singleton паттерн
@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()