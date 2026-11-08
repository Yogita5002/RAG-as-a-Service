# RAG-as-a-Service

A retrieval-augmented generation (RAG) API. Upload PDF or text documents, then ask questions and get answers grounded in those documents, with source citations.

Built with Python, FastAPI, PostgreSQL + pgvector, and open-source LLMs served locally through Ollama.

## How it works

1. **Upload** a `.pdf` or `.txt` via `POST /documents`. Text is extracted with pypdf.
2. **Chunk** the text (800 characters, 150 overlap).
3. **Embed** each chunk with `nomic-embed-text` (768 dimensions).
4. **Store** chunks and vectors in PostgreSQL with pgvector, indexed with HNSW (cosine distance).
5. **Ask** via `POST /query`: the question is embedded and the top 5 closest chunks are retrieved.
6. **Generate** an answer with `llama3.2` (temperature 0.2), instructed to use only the retrieved context and say when it does not know.
7. **Return** the answer plus the source chunks and similarity scores.

The embedding and LLM providers sit behind interfaces (`EmbeddingProvider`, `LLMProvider`), so you can switch between Ollama and an OpenAI-compatible API with one environment variable.

## Run locally with Docker

```bash
docker compose up -d --build
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama pull llama3.2
```

Open http://localhost:8000/docs to try the API.

## Run tests

```bash
pip install -r backend/requirements.txt
pytest -q
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push:

- **pytest** unit tests
- **Docker** image build
- **Terraform** format check and validation

## Infrastructure

`infrastructure/` defines the AWS target architecture in Terraform: ECR, App Runner, RDS PostgreSQL with pgvector, S3, SQS, Secrets Manager and CloudWatch. It is validated in CI but **not currently applied**, to avoid cloud costs. See [infrastructure/README.md](infrastructure/README.md).

## Project structure

```
backend/          FastAPI app, Dockerfile, requirements
  app/api/        HTTP routes (documents, query)
  app/services/   extraction, chunking, embeddings, RAG
  app/providers/  Ollama and OpenAI provider implementations
infrastructure/   Terraform (AWS)
tests/            pytest suite
docs/             architecture notes and diagram
```

## Roadmap

- Async ingestion through SQS workers
- Retrieval evaluation set (hit rate, faithfulness)
- Multi-tenant isolation
- Sentence-aware chunking

## Team

Built for the Essential Cloud and DevOps course by Yogita Y V, Sreeshnav B Sunil and Harshan AM.
