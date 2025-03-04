output "aws_lambda_function_arn" {
  description   = "The ARN of the Lambda ingest function"
  value         = aws_lambda_function.ingest_function.arn
}

# output "aws_cloudwatch_log_group_name" {
#   description   = "The name of the Cloudwatch log group"
#   value         = aws_cloudwatch_log_group.lambda_ingest_log_group.name
# }

# output "cloudwatch_alarm_arn" {
#   description   = "The ARN of Cloudwatch Alarm"
#   value         = aws_cloudwatch_metric_alarm.lambda_ingest_error_alarm.arn
# }

output "aws_state_machine" {
    description = "The ARN for the State Machine"
    value       = aws_sfn_state_machine.sfn_state_machine.name
  
}
