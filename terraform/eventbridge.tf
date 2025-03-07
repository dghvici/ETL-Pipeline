# resource "aws_cloudwatch_event_rule" "s3_object_created" {
#   name        = "s3-eventbridge-rule"
#   description = "Capture S3 object created events"
#   event_pattern = <<EOF
# {
#   "source": ["aws.s3"],
#   "detail-type": ["Object Created"],
#   "detail": {
#     "bucket": {
#       "name": ["your-bucket-name"]
#     }
#   }
# }
# EOF
# }


# resource "aws_cloudwatch_event_target" "lambda_target" {
#   rule      = aws_cloudwatch_event_rule.s3_object_created.name
#   target_id = "SendToLambda"
#   arn       = aws_lambda_function.your_lambda_function.arn
# }


# resource "aws_lambda_permission" "allow_eventbridge" {
#   statement_id  = "AllowExecutionFromEventBridge"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.your_lambda_function.function_name
#   principal     = "events.amazonaws.com"
#   source_arn    = aws_cloudwatch_event_rule.s3_object_created.arn
# }