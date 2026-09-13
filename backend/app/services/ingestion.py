from uuid import UUID

from app.config import get_settings
from app.db import insert_chunks, insert_document
from app.services.chunking import split_text
from app.services.embeddings import embed_texts
from app.services.extraction import extract_text


def ingest_document(filename: str, content_type: str | None, data: bytes) -> tuple[UUID, int]:
    settings = get_settings()
    text = extract_text(filename, data)
    chunks = split_text(text, settings.chunk_size, settings.chunk_overlap)
    embeddings = embed_texts(chunks)
    document_id = insert_document(filename, content_type)
    insert_chunks(document_id, chunks, embeddings, filename)
    return document_id, len(chunks)
