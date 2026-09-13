from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    filename: str
    chunk_count: int


class DocumentListItem(BaseModel):
    id: UUID
    filename: str
    content_type: str | None
    created_at: datetime


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceChunk(BaseModel):
    document_id: UUID
    filename: str
    chunk_index: int
    content: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class HealthResponse(BaseModel):
    status: str
    database: bool
