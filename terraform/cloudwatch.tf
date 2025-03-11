# Cloudwatch log group - defines CW log group for Lambda function
# cloudwatch log stream - for log function
# cloudwatch metric filter - capture function errors 
# cloudwatch alarm - alram triggers which exceed set threshold >90%? 

# outputs.tf file 

# Cloudwatch log group 
resource "aws_cloudwatch_log_group" "lambda_ingest_log_group" {
  name              = aws_s3_bucket.ingestion_bucket.bucket
  retention_in_days = 14
}

# Cloudwatch log stream 
resource "aws_cloudwatch_log_stream" "lambda_ingest_log_stream" {
  name              = "lambda_ingest_log_stream"
  log_group_name    = aws_cloudwatch_log_group.lambda_ingest_log_group.name
}

# Cloudwatch metric filter 
resource "aws_cloudwatch_log_metric_filter" "lambda_ingest_metric_filter" {
  name             = "lambda_ingest_metric_filter"
  log_group_name   = aws_cloudwatch_log_group.lambda_ingest_log_group.name
  pattern          = "ERROR"
  metric_transformation {
    name           = "LambdaErrors"
    namespace      = "LambdaMetrics"
    value          = "1"
  }
}

# SNS to topic Alarms
resource "aws_sns_topic" "cloudwatch_ingest_alarm_topic" {
  name = "cloudwatch-ingest-alarm-topic"
}

# SNS to Gmail 
resource "aws_sns_topic_subscription" "cloudwatch_alarm_subscription" {
  topic_arn     = aws_sns_topic.cloudwatch_ingest_alarm_topic.arn
  protocol      = "email"
  endpoint      = "lullymorewestalerts@gmail.com"
}

# CloudWatch Alarm
resource "aws_cloudwatch_metric_alarm" "lambda_ingest_error_alarm" {
    alarm_name           = "LambdaIngestErrorAlarm"
    comparison_operator  = "GreaterThanOrEqualToThreshold"
    evaluation_periods   = "1"
    metric_name          = aws_cloudwatch_log_metric_filter.lambda_ingest_metric_filter.metric_transformation[0].name
    namespace            = aws_cloudwatch_log_metric_filter.lambda_ingest_metric_filter.metric_transformation[0].namespace
    period               = "60"
    statistic            = "Sum"
    threshold            = "1"

    alarm_description    = "Alarm when Lambda ingest function errors exceed 1"
    actions_enabled      = true

    alarm_actions        = [
        aws_sns_topic.cloudwatch_ingest_alarm_topic.arn
    ]
}

