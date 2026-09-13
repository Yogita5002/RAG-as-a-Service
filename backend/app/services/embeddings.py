from app.config import get_settings
from app.exceptions import EmbeddingDimensionError
from app.providers.factory import get_embedding_provider


def _validate_dimension(embedding: list[float], index: int | None = None) -> None:
    expected = get_settings().embedding_dimension
    actual = len(embedding)
    if actual != expected:
        where = f" at index {index}" if index is not None else ""
        raise EmbeddingDimensionError(
            f"Embedding{where} has dimension {actual}, expected {expected}"
        )


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = get_embedding_provider().embed_texts(texts)
    if len(vectors) != len(texts):
        raise EmbeddingDimensionError(
            f"Provider returned {len(vectors)} embeddings for {len(texts)} texts"
        )
    for index, vector in enumerate(vectors):
        _validate_dimension(vector, index)
    return vectors


def embed_query(text: str) -> list[float]:
    vector = get_embedding_provider().embed_query(text)
    _validate_dimension(vector)
    return vector
