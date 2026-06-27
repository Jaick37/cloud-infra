terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "todo-app-server"
  }
}

resource "aws_s3_bucket" "static_assets" {
  bucket = "jaick-todo-app-static-assets"
}

resource "aws_db_instance" "todo_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  db_name              = "tododb"
  username             = "postgres"
  password             = var.db_password
  skip_final_snapshot  = true
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
