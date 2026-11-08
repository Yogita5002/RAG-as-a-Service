variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Prefix used for resource names"
  type        = string
  default     = "rag-as-a-service"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "rag"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "rag_admin"
}

variable "db_instance_class" {
  description = "RDS instance size"
  type        = string
  default     = "db.t4g.micro"
}

variable "image_tag" {
  description = "Container image tag App Runner deploys from ECR"
  type        = string
  default     = "latest"
}

variable "model_provider" {
  description = "LLM/embedding provider the API uses in the cloud (ollama or openai-compatible)"
  type        = string
  default     = "openai"
}

variable "llm_model" {
  description = "Chat model name"
  type        = string
  default     = "llama3.2"
}

variable "embedding_model" {
  description = "Embedding model name"
  type        = string
  default     = "nomic-embed-text"
}

variable "embedding_dimension" {
  description = "Vector size produced by the embedding model"
  type        = number
  default     = 768
}
