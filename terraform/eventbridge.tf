#IAM Role for Eventbridge
resource "aws_iam_role" "eventbridge_role" {
  name = "eventbridge-invoke-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

#Attaching Permissions to Invoke Lambdas (ingest AND transform)
resource "aws_iam_policy" "eventbridge_lambda_policy" {
  name        = "EventBridgeLambdaInvokePolicy"
  description = "Allows EventBridge to invoke Lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
        {
        Action = [
            "lambda:InvokeFunction",
        ]
        Effect      = "Allow",
        Resource    = "*"
        },
        ]
    })
}

#Lambda Policy attachment to IAM (from above)
resource "aws_iam_role_policy_attachment" "eventbridge_lambda_attach" {
  role       = aws_iam_role.eventbridge_role.name
  policy_arn = aws_iam_policy.eventbridge_lambda_policy.arn
}

############################### TRANSFORM ##################################

#Rule for Ingestion Bucket
resource "aws_cloudwatch_event_rule" "s3_object_created_transform" {
  name        = "s3-eventbridge-rule-transform"
  description = "Capture S3 object created events"
  event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["etl-lullymore-west-ingested"]
    }
  }
}
EOF
}

#Lambda Target > Transform
resource "aws_cloudwatch_event_target" "lambda_target_transform" {
  rule      = aws_cloudwatch_event_rule.s3_object_created_transform.name
  target_id = "SendToLambda"
  arn       = aws_lambda_function.transform_function.arn
}


resource "aws_lambda_permission" "allow_eventbridge_transform" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_object_created_transform.arn
}

############################## LOAD ######################################

#Rule for Transformed Bucket
resource "aws_cloudwatch_event_rule" "s3_object_created_load" {
  name        = "s3-eventbridge-rule-load"
  description = "Capture S3 object created events"
  event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["etl-lullymore-west-transformed"]
    }
  }
}
EOF
}

resource "aws_cloudwatch_event_target" "lambda_target_load" {
  rule      = aws_cloudwatch_event_rule.s3_object_created_load.name
  target_id = "SendToLambda"
  arn       = aws_lambda_function.load_function.arn
}


resource "aws_lambda_permission" "allow_eventbridge_load" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.load_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_object_created_load.arn
}


######################## S3 NOTIFICATIONS ############################

########## INGESTION BUCKET > TRANSFORM FUNCTION ################

resource "aws_lambda_permission" "allow_bucket_ingest" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.ingestion_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification_ingest" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.transform_function.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "AWSLogs/"
    filter_suffix       = ".log"
  }

  depends_on = [aws_lambda_permission.allow_bucket_ingest]
}

########## TRANSFORMED BUCKET > LOAD FUNCTION #################

resource "aws_lambda_permission" "allow_bucket_transform" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.load_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.transform_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification_transform" {
  bucket = aws_s3_bucket.transform_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.load_function.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "AWSLogs/"
    filter_suffix       = ".log"
  }

  depends_on = [aws_lambda_permission.allow_bucket_transform]
} 