from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Iterator
from uuid import UUID, uuid4

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.config import get_settings
from app.exceptions import DatabaseError, EmbeddingDimensionError

logger = logging.getLogger(__name__)


@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    settings = get_settings()
    if not settings.database_url:
        raise DatabaseError("DATABASE_URL is not configured")
    try:
        conn = psycopg.connect(settings.database_url, row_factory=dict_row)
    except psycopg.Error as exc:
        raise DatabaseError(f"Could not connect to the database: {exc}") from exc
    try:
        register_vector(conn)
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create extension and tables. Replace this function with migrations later."""
    settings = get_settings()
    dimension = settings.embedding_dimension
    if not settings.database_url:
        raise DatabaseError("DATABASE_URL is not configured")

    # The vector type must exist before register_vector() runs in get_connection(),
    # so create the extension on a plain connection first.
    try:
        with psycopg.connect(settings.database_url, autocommit=True) as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    except psycopg.Error as exc:
        raise DatabaseError(f"Could not create pgvector extension: {exc}") from exc

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY,
                filename TEXT NOT NULL,
                content_type TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS chunks (
                id UUID PRIMARY KEY,
                document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding vector({dimension}) NOT NULL,
                metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw_idx
            ON chunks
            USING hnsw (embedding vector_cosine_ops)
            """
        )
    logger.info("Database schema initialized (embedding dimension=%s)", dimension)


def ping() -> bool:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        logger.exception("Database ping failed")
        return False


def _assert_embedding_dimension(embedding: list[float], index: int | None = None) -> None:
    expected = get_settings().embedding_dimension
    actual = len(embedding)
    if actual != expected:
        where = f" at index {index}" if index is not None else ""
        raise EmbeddingDimensionError(
            f"Embedding{where} has dimension {actual}, expected {expected}"
        )


def insert_document(filename: str, content_type: str | None) -> UUID:
    document_id = uuid4()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO documents (id, filename, content_type)
            VALUES (%s, %s, %s)
            """,
            (document_id, filename, content_type),
        )
    return document_id


def insert_chunks(
    document_id: UUID,
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
) -> int:
    if len(chunks) != len(embeddings):
        raise EmbeddingDimensionError(
            f"Chunk count ({len(chunks)}) does not match embedding count ({len(embeddings)})"
        )

    for index, embedding in enumerate(embeddings):
        _assert_embedding_dimension(embedding, index)

    with get_connection() as conn:
        for index, (content, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
            conn.execute(
                """
                INSERT INTO chunks (
                    id, document_id, chunk_index, content, embedding, metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    uuid4(),
                    document_id,
                    index,
                    content,
                    embedding,
                    Jsonb({"filename": filename, "chunk_index": index}),
                ),
            )
    return len(chunks)


def list_documents() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, filename, content_type, created_at
            FROM documents
            ORDER BY created_at DESC
            """
        ).fetchall()
    return list(rows)


def search_chunks(query_embedding: list[float], top_k: int) -> list[dict[str, Any]]:
    _assert_embedding_dimension(query_embedding)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                c.id,
                c.document_id,
                c.chunk_index,
                c.content,
                d.filename,
                1 - (c.embedding <=> %s::vector) AS score
            FROM chunks c
            JOIN documents d ON d.id = c.document_id
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
            """,
            (query_embedding, query_embedding, top_k),
        ).fetchall()
    return list(rows)