from fastapi import APIRouter

from app.schemas import QueryRequest, QueryResponse
from app.services.rag import answer_question

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_documents(payload: QueryRequest) -> QueryResponse:
    answer, sources = answer_question(payload.question, payload.top_k)
    return QueryResponse(answer=answer, sources=sources)
