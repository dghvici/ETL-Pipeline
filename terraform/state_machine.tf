# step function state machine 
# Ingest, 
# second stagetransform, load - repeat State x2 
# reseource used: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine 
# might need to check nameing conventions once everything is merged 

resource "aws_sfn_state_machine" "sfn_state_machine" {
  name       = "IngestTransformLoadStepFunctionStateMachine"
  role_arn   = aws_iam_role.iam_for_lambda.arn

  definition = jsonencode({
    Comment = "An AWS Step Functions state manchine which ingests, transforms and loads data"
    StartAt = "IngestData",
    States  = {
        IngestData = {
            Type        = "Task",
            Resource    = aws_lambda_function.ingest_function.arn
            End         = true
        }
    }
  })
}

