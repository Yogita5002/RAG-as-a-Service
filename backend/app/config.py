from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_env: str = "development"
    database_url: str = ""

    provider: str = Field(default="ollama", validation_alias="MODEL_PROVIDER")

    ollama_host: str = "http://127.0.0.1:11434"

    openai_api_key: str = ""
    openai_base_url: str | None = None

    embedding_model: str = "nomic-embed-text"
    llm_model: str = "llama3.2"
    embedding_dimension: int = 768

    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 5

    @field_validator("embedding_dimension")
    @classmethod
    def validate_embedding_dimension(cls, value: int) -> int:
        if value < 1 or value > 8192:
            raise ValueError("EMBEDDING_DIMENSION must be between 1 and 8192")
        return value

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, value: int, info) -> int:
        chunk_size = info.data.get("chunk_size", 800)
        if value < 0:
            raise ValueError("CHUNK_OVERLAP must be >= 0")
        if value >= chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return value

    @field_validator("openai_base_url", mode="before")
    @classmethod
    def empty_base_url_to_none(cls, value: str | None) -> str | None:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
