from fastapi import APIRouter, File, UploadFile

from app.db import list_documents
from app.exceptions import EmptyDocumentError
from app.schemas import DocumentListItem, DocumentUploadResponse
from app.services.ingestion import ingest_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    filename = file.filename or "upload"
    data = await file.read()
    if not data:
        raise EmptyDocumentError("Uploaded file is empty")
    document_id, chunk_count = ingest_document(filename, file.content_type, data)
    return DocumentUploadResponse(
        document_id=document_id,
        filename=filename,
        chunk_count=chunk_count,
    )


@router.get("", response_model=list[DocumentListItem])
def get_documents() -> list[DocumentListItem]:
    rows = list_documents()
    return [DocumentListItem(**row) for row in rows]
