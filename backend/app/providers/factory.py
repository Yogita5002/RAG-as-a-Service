from functools import lru_cache

from app.config import get_settings
from app.exceptions import ProviderConfigError
from app.providers.base import EmbeddingProvider, LLMProvider
from app.providers.ollama import OllamaEmbeddingProvider, OllamaLLMProvider
from app.providers.openai import OpenAIEmbeddingProvider, OpenAILLMProvider


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    name = settings.provider.lower().strip()
    if name == "ollama":
        return OllamaEmbeddingProvider(
            model=settings.embedding_model,
            host=settings.ollama_host,
        )
    if name == "openai":
        return OpenAIEmbeddingProvider(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
            base_url=settings.openai_base_url,
        )
    raise ProviderConfigError(
        f"Unsupported MODEL_PROVIDER '{settings.provider}'. Supported: ollama, openai"
    )


@lru_cache
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    name = settings.provider.lower().strip()
    if name == "ollama":
        return OllamaLLMProvider(
            model=settings.llm_model,
            host=settings.ollama_host,
        )
    if name == "openai":
        return OpenAILLMProvider(
            api_key=settings.openai_api_key,
            model=settings.llm_model,
            base_url=settings.openai_base_url,
        )
    raise ProviderConfigError(
        f"Unsupported MODEL_PROVIDER '{settings.provider}'. Supported: ollama, openai"
    )


def reset_providers() -> None:
    get_embedding_provider.cache_clear()
    get_llm_provider.cache_clear()
