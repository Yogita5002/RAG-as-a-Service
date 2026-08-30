# RAG as a Service

A multi-tenant Retrieval-Augmented Generation platform built on AWS.

## Overview

RAG as a Service allows client organizations to upload their own documents
and ask questions about their content using natural language.

The system retrieves relevant document chunks and provides them as context
to a Large Language Model to generate grounded answers with source citations.

The platform is designed to support multiple tenants while maintaining
strict tenant-level data isolation.

## Planned Architecture

- Amazon S3 — document storage
- Amazon SQS — asynchronous processing
- AWS Lambda — ingestion worker
- Amazon RDS PostgreSQL + pgvector — database and vector search
- FastAPI — API layer
- Amazon ECR — container registry
- AWS App Runner — application deployment
- AWS Secrets Manager — secrets management
- Amazon CloudWatch — monitoring
- Terraform — Infrastructure as Code
- GitHub Actions — CI/CD

## Development Roadmap

1. Local RAG pipeline
2. AWS deployment
3. Asynchronous document ingestion
4. Containerization
5. Infrastructure as Code
6. CI/CD
7. Multi-tenancy and security
8. Monitoring and observability
9. Automated retrieval evaluation

## Team

- Yogita.Y.V
- Sreeshnav B Sunil
- Harshan AM


## Course

Essential Cloud and DevOps

## Status

🚧 Under development

![System Architecture](image.png)