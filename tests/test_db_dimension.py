from app.config import get_settings
from app.db import _assert_embedding_dimension
from app.exceptions import EmbeddingDimensionError
import pytest


def test_db_rejects_mismatched_embedding_dimension():
    with pytest.raises(EmbeddingDimensionError):
        _assert_embedding_dimension([0.1, 0.2], index=0)


def test_db_accepts_configured_embedding_dimension():
    vector = [0.0] * get_settings().embedding_dimension
    _assert_embedding_dimension(vector)
