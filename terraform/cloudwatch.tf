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

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "cloudwatch_policy_attachment" {
    role       = aws_iam_role.cloudwatch_role.name
    policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

resource "aws_cloudwatch_event_rule" "every_half_hour" {
  name                  = "EveryHalfHour"
  description           = "Trigger Ingest Lambda function at the 0 and 30th minute of every hour" 
  schedule_expression   = "cron(0,30 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "target" {
  rule      = aws_cloudwatch_event_rule.every_half_hour
  target_id = ingest_lambda
  arn       = aws_lambda_function.ingest_function.arn 

}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudwatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_half_hour.arn
}