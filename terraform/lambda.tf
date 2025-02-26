data "archive_file" "ingest_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/extract/function_ingest.zip"
  source_file = "${path.module}/../src/lambda_ingest.py"
}

data "archive_file" "transform_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/transform/function_transform.zip"
  source_file = "${path.module}/../src/lambda_transform.py"
}

data "archive_file" "load_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/load/function_load.zip"
  source_file = "${path.module}/../src/lambda_load.py"
}


resource "aws_lambda_function" "ingest_function" {
  filename      = data.archive_file.ingest_lambda.output_path
  function_name = "ingest_function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler_ingest"
  runtime       = "python3.12"

  source_code_hash = data.archive_file.ingest_lambda.output_base64sha512

}

resource "aws_lambda_function" "transform_function" {
  filename      = data.archive_file.transform_lambda.output_path
  function_name = "transform_function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler_transform"
  runtime       = "python3.12"

  source_code_hash = data.archive_file.transform_lambda.output_base64sha512
}

resource "aws_lambda_function" "load_function" {
  filename      = data.archive_file.load_lambda.output_path
  function_name = "load_function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler_load"
  runtime       = "python3.12"

  source_code_hash = data.archive_file.load_lambda.output_base64sha512
}


resource "aws_iam_role" "lambda_role" {
  name_prefix        = "role-currency-lambdas-"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    EOF
}