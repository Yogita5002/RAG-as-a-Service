from uuid import uuid4

from app.services.rag import SYSTEM_PROMPT, build_user_prompt


def test_build_user_prompt_includes_sources_and_question():
    sources = [
        {
            "filename": "guide.pdf",
            "chunk_index": 0,
            "content": "pgvector stores embeddings in PostgreSQL.",
        }
    ]
    prompt = build_user_prompt("What is pgvector?", sources)
    assert "guide.pdf" in prompt
    assert "pgvector stores embeddings" in prompt
    assert "What is pgvector?" in prompt


def test_build_user_prompt_without_sources():
    prompt = build_user_prompt("Anything?", [])
    assert "(none)" in prompt
    assert "do not know" in prompt


def test_system_prompt_requires_grounding():
    assert "only the provided context" in SYSTEM_PROMPT


def test_query_endpoint_returns_answer_and_sources(client, monkeypatch):
    document_id = uuid4()

    def fake_answer(question, top_k=None):
        from app.schemas import SourceChunk

        source = SourceChunk(
            document_id=document_id,
            filename="guide.pdf",
            chunk_index=0,
            content="pgvector stores embeddings in PostgreSQL.",
            score=0.91,
        )
        return "pgvector stores embeddings in PostgreSQL.", [source]

    monkeypatch.setattr("app.api.query.answer_question", fake_answer)
    response = client.post("/query", json={"question": "What is pgvector?"})
    assert response.status_code == 200
    body = response.json()
    assert "pgvector" in body["answer"]
    assert body["sources"][0]["filename"] == "guide.pdf"
