from io import BytesIO
from uuid import uuid4

from app.exceptions import AppError


def test_upload_document_endpoint(client, monkeypatch):
    document_id = uuid4()

    def fake_ingest(filename, content_type, data):
        assert filename == "notes.txt"
        assert data == b"hello rag"
        return document_id, 1

    monkeypatch.setattr("app.api.documents.ingest_document", fake_ingest)
    response = client.post(
        "/documents",
        files={"file": ("notes.txt", BytesIO(b"hello rag"), "text/plain")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["document_id"] == str(document_id)
    assert body["chunk_count"] == 1


def test_upload_rejects_empty_file(client):
    response = client.post(
        "/documents",
        files={"file": ("notes.txt", BytesIO(b""), "text/plain")},
    )
    assert response.status_code == 400


def test_list_documents_endpoint(client, monkeypatch):
    document_id = uuid4()
    monkeypatch.setattr(
        "app.api.documents.list_documents",
        lambda: [
            {
                "id": document_id,
                "filename": "notes.txt",
                "content_type": "text/plain",
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ],
    )
    response = client.get("/documents")
    assert response.status_code == 200
    assert response.json()[0]["filename"] == "notes.txt"


def test_app_error_handler(client, monkeypatch):
    def boom(*_args, **_kwargs):
        raise AppError("no database", status_code=503)

    monkeypatch.setattr("app.api.documents.list_documents", boom)
    response = client.get("/documents")
    assert response.status_code == 503
    assert response.json()["detail"] == "no database"
