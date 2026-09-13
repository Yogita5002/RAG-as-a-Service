from app.config import get_settings
from app.db import search_chunks
from app.schemas import SourceChunk
from app.services.embeddings import embed_query
from app.services.llm import generate_answer

SYSTEM_PROMPT = (
    "You are a retrieval-augmented assistant. "
    "Answer the user's question using only the provided context. "
    "If the context is insufficient, say you do not know. "
    "Do not invent facts. Mention source filenames when they support the answer."
)


def build_user_prompt(question: str, sources: list[dict]) -> str:
    if not sources:
        return (
            "Context:\n(none)\n\n"
            f"Question: {question}\n\n"
            "There is no retrieved context. Say you do not know."
        )

    blocks = []
    for i, source in enumerate(sources, start=1):
        blocks.append(
            f"[{i}] {source['filename']} (chunk {source['chunk_index']}):\n{source['content']}"
        )
    context = "\n\n".join(blocks)
    return f"Context:\n{context}\n\nQuestion: {question}"


def answer_question(question: str, top_k: int | None = None) -> tuple[str, list[SourceChunk]]:
    settings = get_settings()
    k = top_k or settings.top_k
    query_embedding = embed_query(question)
    rows = search_chunks(query_embedding, k)

    answer = generate_answer(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=build_user_prompt(question, rows),
    )
    sources = [
        SourceChunk(
            document_id=row["document_id"],
            filename=row["filename"],
            chunk_index=row["chunk_index"],
            content=row["content"],
            score=float(row["score"]),
        )
        for row in rows
    ]
    return answer, sources
