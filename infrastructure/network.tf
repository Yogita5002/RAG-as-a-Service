# Use the account's default VPC to keep the setup small.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# App Runner reaches the database through this security group.
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app"
  description = "App Runner VPC connector"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# The database accepts PostgreSQL traffic only from the app.
resource "aws_security_group" "db" {
  name        = "${var.project_name}-db"
  description = "RDS PostgreSQL"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

resource "aws_apprunner_vpc_connector" "this" {
  vpc_connector_name = "${var.project_name}-vpc"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.app.id]
}
