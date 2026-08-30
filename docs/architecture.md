# Architecture

## Ingestion Flow

Client
→ FastAPI
→ S3
→ SQS
→ Lambda Worker
→ Chunking
→ Embeddings
→ PostgreSQL + pgvector

## Query Flow

Client
→ FastAPI
→ Tenant Authentication
→ Query Embedding
→ PostgreSQL + pgvector
→ Top-K Retrieval
→ Prompt Construction
→ LLM
→ Answer + Source Citations

## Core Principles

- Multi-tenancy
- Tenant data isolation
- Asynchronous processing
- Cloud-native deployment
- Infrastructure as Code
- CI/CD
- Monitoring
- Automated retrieval evaluation
