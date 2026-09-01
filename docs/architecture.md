# RAG as a Service — Architecture

## Overview

RAG as a Service is a multi-tenant Retrieval-Augmented Generation platform that allows organizations to upload documents and ask natural-language questions about their content.

The platform uses asynchronous document ingestion and synchronous RAG query processing.

---

## High-Level Architecture

```text
Users / Tenants
       |
       v
React + Vite Frontend
       |
       v
Amazon API Gateway
       |
       v
FastAPI Backend
       |
       +--------------------+
       |                    |
       v                    v
Document Ingestion       Query / RAG Flow
       |                    |
       v                    v
     Amazon S3          Authentication
       |                    |
       v                    v
    Amazon SQS         Query Embedding
       |                    |
       v                    v
   AWS Lambda          OpenSearch
       |                    |
       v                    v
Text Extraction         Top-K Retrieval
Chunking                    |
Embeddings                  v
       |              Prompt Construction
       v                    |
Amazon OpenSearch           v
       |              Amazon Bedrock LLM
       |                    |
       +--------------------+
                            |
                            v
                  Answer + Source Citations
                            |
                            v
                       React Frontend