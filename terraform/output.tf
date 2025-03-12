output "aws_lambda_function_arn" {
  description   = "The ARN of the Lambda ingest function"
  value         = aws_lambda_function.ingest_function.arn
}

# output "aws_state_machine" {
#     description = "The ARN for the State Machine"
#     value       = aws_sfn_state_machine.sfn_state_machine.name
# }
