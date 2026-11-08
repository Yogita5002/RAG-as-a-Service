output "api_url" {
  description = "Public URL of the API"
  value       = "https://${aws_apprunner_service.api.service_url}"
}

output "ecr_repository_url" {
  description = "Push the backend image here"
  value       = aws_ecr_repository.backend.repository_url
}

output "documents_bucket" {
  value = aws_s3_bucket.documents.bucket
}

output "ingestion_queue_url" {
  value = aws_sqs_queue.ingestion.url
}
