import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "")
os.environ.setdefault("MODEL_PROVIDER", "ollama")
os.environ.setdefault("OLLAMA_HOST", "http://127.0.0.1:11434")
os.environ.setdefault("EMBEDDING_MODEL", "nomic-embed-text")
os.environ.setdefault("LLM_MODEL", "llama3.2")

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.providers.factory import reset_providers


@pytest.fixture(autouse=True)
def _reset_caches():
    get_settings.cache_clear()
    reset_providers()
    yield
    get_settings.cache_clear()
    reset_providers()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
