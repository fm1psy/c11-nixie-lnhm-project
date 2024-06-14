provider "aws" {
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
    region = var.AWS_REGION
}

resource "aws_ecs_cluster" "c11-cluster" {
    name = "c11-cluster"
}

# roles and permissions

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

data "aws_iam_policy_document" "eventbridge_role" {
    statement {
        effect = "Allow"
        principals {
            type = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
    
}

resource "aws_iam_role" "iam_for_lambda" {
    name               = "iam_for_lambda"
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
resource "aws_iam_role" "iam_for_eventbridge" {
    name               = "iam_for_eventbridge"
    assume_role_policy = data.aws_iam_policy_document.eventbridge_role.json
}

# ETL lambda
resource "aws_lambda_function" "c11-nixie-lnhm-etl-lambda" {
    function_name = "c11-nixie-lnhm-etl-lambda"
    role          = aws_iam_role.iam_for_lambda.arn
    package_type  = "Image"
    image_uri     = var.PIPELINE_URI
    architectures = ["x86_64"]
    timeout       = 120

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

# translocation lambda
resource "aws_s3_bucket" "c11-nixie-lts-bucket" {
    bucket = "nixie-lmnh-plants-lts"
    force_destroy = true
}

# resource "aws_lambda_function" "c11-nixie-lnhm-data-translocation" {
#     function_name = "c11-nixie-lnhm-data-translocation"
#     role          = aws_iam_role.iam_for_lambda.arn
#     package_type  = "Image"
#     image_uri     = var.TRANSLOCATION_URI
#     architectures = ["x86_64"]
#     timeout       = 15

#     environment {
#         variables = {
#         DB_HOST     = var.DB_HOST
#         DB_NAME     = var.DB_NAME
#         DB_PASSWORD = var.DB_PASSWORD
#         DB_PORT     = var.DB_PORT
#         DB_SCHEMA   = var.DB_SCHEMA
#         DB_USER     = var.DB_USER
#         }
#     }
# }
# schedulers
resource "aws_scheduler_schedule" "c11-nixie-lnhm-etl-scheduler" {
  name       = "c11-nixie-lnhm-etl-scheduler"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(* * * * ? *)"

  target {
    arn      = aws_lambda_function.c11-nixie-lnhm-etl-lambda.arn
    role_arn = aws_iam_role.iam_for_eventbridge.arn
  }
}

# resource "aws_scheduler_schedule" "c11-nixie-lnhm-translocation-schedule" {
#   name       = "c11-nixie-lnhm-translocation-schedule"
#   group_name = "default"

#   flexible_time_window {
#     mode = "OFF"
#   }

#   schedule_expression = "cron(0 9 * * ? *)"

#   target {
#     arn      = aws_lambda_function.c11-nixie-lnhm-data-translocation.arn
#     role_arn = aws_iam_role.iam_for_lambda.arn
#   }
# }
# dashboard service
