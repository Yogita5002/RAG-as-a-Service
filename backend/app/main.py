import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.documents import router as documents_router
from app.api.query import router as query_router
from app.db import init_db, ping
from app.exceptions import AppError
from app.schemas import HealthResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        init_db()
    except AppError:
        logger.exception("Database initialization skipped or failed")
    yield


app = FastAPI(
    title="RAG as a Service",
    description=(
        "Local retrieval-augmented generation API. "
        "Upload PDF or text documents, then ask questions grounded in retrieved chunks."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    database_ok = ping()
    return HealthResponse(
        status="healthy" if database_ok else "degraded",
        database=database_ok,
    )


app.include_router(documents_router)
app.include_router(query_router)
