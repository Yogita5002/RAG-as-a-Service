# Infrastructure (Terraform)

AWS infrastructure for RAG-as-a-Service, written as code. It is **validated in CI but not applied**, so there is no running AWS deployment and no cost.

## What it defines

| File | Resources |
| --- | --- |
| `storage.tf` | S3 bucket for documents (private, encrypted), SQS ingestion queue + dead-letter queue, ECR repository |
| `database.tf` | RDS PostgreSQL 16 (pgvector-capable), random password, `DATABASE_URL` in Secrets Manager |
| `network.tf` | Security groups (DB accepts traffic only from the app), App Runner VPC connector, default VPC lookup |
| `app.tf` | App Runner service running the backend image, IAM roles (ECR pull; runtime access to secret, bucket, queue), CloudWatch log group |
| `outputs.tf` | API URL, ECR URL, bucket name, queue URL |

## Commands

```bash
cd infrastructure
terraform init
terraform fmt -check
terraform validate
terraform plan          # needs AWS credentials
# terraform apply       # would create billable resources
```

GitHub Actions runs `fmt -check`, `init -backend=false` and `validate` on every push.
