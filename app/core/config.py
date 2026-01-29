from functools import lru_cache
from typing import Literal, Optional

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/self_rag")


class EmbeddingsSettings(BaseModel):
    provider: Literal["stub", "openai", "hf"] = "stub"
    dim: int = 384
    openai_model: str = "text-embedding-3-small"
    hf_model: Optional[str] = None


class VectorIndexSettings(BaseModel):
    provider: Literal["in_memory", "faiss"] = "in_memory"
    persist_path: str = "./data/vector_index.faiss"


class WorkerSettings(BaseModel):
    poll_interval_seconds: float = 1.0
    max_batch_size: int = 32
    quality_threshold: float = 0.6


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SELF_RAG_", env_file=".env", extra="ignore")

    api_prefix: str = "/api/v1"
    project_name: str = "Self-RAG Backend"
    database: DatabaseSettings = DatabaseSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    vector_index: VectorIndexSettings = VectorIndexSettings()
    worker: WorkerSettings = WorkerSettings()
    allowed_origins: list[AnyHttpUrl] = []


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

