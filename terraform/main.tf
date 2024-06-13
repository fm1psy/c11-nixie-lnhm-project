provider "aws" {
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
    region = var.AWS_REGION
}

resource "aws_ecs_cluster" "c11-cluster" {
    name = "c11-cluster"
}

# ETL lambda

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_lambda_function" "c11-nixie-lnhm-etl" {
    function_name = "c11-nixie-lnhm-etl"
    role          = aws_iam_role.iam_for_lambda.arn
    package_type  = "Image"
    image_uri     = var.PIPELINE_URI
    architectures = ["x86_64"]
    timeout       = 15

    environment {
        variables = {
        DB_HOST     = var.DB_HOST
        DB_NAME     = var.DB_NAME
        DB_PASSWORD = var.DB_PASSWORD
        DB_PORT     = var.DB_PORT
        DB_SCHEMA   = var.DB_SCHEMA
        DB_USER     = var.DB_USER
        }
    }
}

resource "aws_s3_bucket" "c11-nixie-lts-bucket" {
    bucket = "nixie-lmnh-plants-lts"
    force_destroy = True
}