#TO BE DELETED AFTER SUCCESFUL DEPLOYMENT

# resource "aws_sfn_state_machine" "sfn_state_machine" {
#   name       = "IngestTransformLoadStepFunctionStateMachine"
#   role_arn   = aws_iam_role.iam_for_lambda.arn

#   definition = jsonencode({
#     Comment = "An AWS Step Functions state manchine which ingests, transforms and loads data"
#     StartAt = "IngestData",
#     States  = {
#         IngestData = {
#             Type        = "Task",
#             Resource    = aws_lambda_function.ingest_function.arn
#             End         = true
#         }
#     }
#   })
# }

