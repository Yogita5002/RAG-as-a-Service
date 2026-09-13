from types import SimpleNamespace

import pytest

from app.config import get_settings
from app.exceptions import EmbeddingDimensionError, ProviderConfigError
from app.providers.factory import get_embedding_provider, get_llm_provider, reset_providers
from app.providers.ollama import OllamaEmbeddingProvider, OllamaLLMProvider
from app.providers.openai import OpenAIEmbeddingProvider, OpenAILLMProvider
from app.services import embeddings as embeddings_service


def test_factory_returns_ollama_providers():
    embedding_provider = get_embedding_provider()
    llm_provider = get_llm_provider()
    assert isinstance(embedding_provider, OllamaEmbeddingProvider)
    assert isinstance(llm_provider, OllamaLLMProvider)


def test_factory_returns_openai_providers_when_selected(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    get_settings.cache_clear()
    reset_providers()
    assert isinstance(get_embedding_provider(), OpenAIEmbeddingProvider)
    assert isinstance(get_llm_provider(), OpenAILLMProvider)


def test_factory_rejects_unknown_provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "unknown")
    get_settings.cache_clear()
    reset_providers()
    with pytest.raises(ProviderConfigError):
        get_embedding_provider()


def test_embed_texts_rejects_wrong_dimension(monkeypatch):
    class FakeProvider:
        def embed_texts(self, texts):
            return [[0.1, 0.2, 0.3] for _ in texts]

        def embed_query(self, text):
            return [0.1, 0.2, 0.3]

    monkeypatch.setattr(embeddings_service, "get_embedding_provider", lambda: FakeProvider())
    with pytest.raises(EmbeddingDimensionError):
        embeddings_service.embed_texts(["hello"])


def test_embed_query_accepts_configured_dimension(monkeypatch):
    dimension = get_settings().embedding_dimension

    class FakeProvider:
        def embed_texts(self, texts):
            return [[0.0] * dimension for _ in texts]

        def embed_query(self, text):
            return [0.0] * dimension

    monkeypatch.setattr(embeddings_service, "get_embedding_provider", lambda: FakeProvider())
    vector = embeddings_service.embed_query("hello")
    assert len(vector) == dimension


def test_ollama_embed_texts_uses_mocked_client(monkeypatch):
    dimension = get_settings().embedding_dimension
    fake_client = SimpleNamespace()

    def fake_embed(model, input):
        assert model == "nomic-embed-text"
        return {"embeddings": [[0.1] * dimension for _ in input]}

    fake_client.embed = fake_embed
    monkeypatch.setattr("app.providers.ollama.ollama.Client", lambda host: fake_client)

    provider = OllamaEmbeddingProvider(model="nomic-embed-text", host="http://127.0.0.1:11434")
    vectors = provider.embed_texts(["hello", "world"])
    assert len(vectors) == 2
    assert len(vectors[0]) == dimension


def test_ollama_generate_uses_mocked_client(monkeypatch):
    fake_client = SimpleNamespace()

    def fake_chat(model, messages, options):
        assert model == "llama3.2"
        assert messages[0]["role"] == "system"
        return {"message": {"content": "grounded answer"}}

    fake_client.chat = fake_chat
    monkeypatch.setattr("app.providers.ollama.ollama.Client", lambda host: fake_client)

    provider = OllamaLLMProvider(model="llama3.2", host="http://127.0.0.1:11434")
    answer = provider.generate(system_prompt="sys", user_prompt="q")
    assert answer == "grounded answer"
