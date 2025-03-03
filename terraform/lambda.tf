data "archive_file" "ingest_lambda" {
  type        = "zip"
  output_file_mode = "0666"
  output_path = "${path.module}/../packages/extract/function_ingest.zip"
  source_file = "${path.module}/../src/lambda_ingest.py"
}

data "archive_file" "transform_lambda" {
  type        = "zip"
  output_file_mode = "0666"
  output_path = "${path.module}/../packages/transform/function_transform.zip"
  source_file = "${path.module}/../src/lambda_transform.py"
}

data "archive_file" "load_lambda" {
  type        = "zip"
  output_file_mode = "0666"
  output_path = "${path.module}/../packages/load/function_load.zip"
  source_file = "${path.module}/../src/lambda_load.py"
}


resource "aws_lambda_function" "ingest_function" {
  filename      = data.archive_file.ingest_lambda.output_path
  function_name = var.ingest_lambda
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_ingest.lambda_handler_ingest"
  runtime       = "python3.12"
  layers        = [aws_lambda_layer_version.utils_layer.arn]
  timeout       = var.default_timeout
  source_code_hash = data.archive_file.ingest_lambda.output_base64sha512
  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.ingestion_bucket.bucket
    }
  }
}

resource "aws_lambda_function" "transform_function" {
  filename      = data.archive_file.transform_lambda.output_path
  function_name = var.transform_lambda
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_transform.lambda_handler_transform"
  runtime       = "python3.12"
  layers        = [aws_lambda_layer_version.utils_layer.arn]
  source_code_hash = data.archive_file.transform_lambda.output_base64sha512
  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.transform_bucket.bucket
    }
  }
}

resource "aws_lambda_function" "load_function" {
  filename      = data.archive_file.load_lambda.output_path
  function_name = var.load_lambda
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_load.lambda_handler_load"
  runtime       = "python3.12"
  layers        = [aws_lambda_layer_version.utils_layer.arn]
  source_code_hash = data.archive_file.load_lambda.output_base64sha512
}


data "archive_file" "layer" {
  type        = "zip"
  output_file_mode = "0666"
  output_path = "${path.module}/../layers.zip"
  source_dir = "${path.module}/../layer/"
}

resource "aws_lambda_layer_version" "utils_layer" {
  filename   = "${path.module}/../layers.zip"
  layer_name = "lambda_utils_layer"

  compatible_runtimes = ["python3.12"]
}



