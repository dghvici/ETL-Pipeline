data "aws_iam_policy_document" "cloudwatch_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:GetLogEvents",
      "logs:FilterLogEvents"
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "cloudwatch:PutMetricData",
      "cloudwatch:GetMetricStatistics",
      "cloudwatch:ListMetrics",
      "cloudwatch:ListMetricStreams",
      "cloudwatch:StartMetricStreams",
      "cloudwatch:StopMetricStreams",
      "cloudwatch:SetAlarmState",
      "cloudwatch:PutMetricAlarm",
      "cloudwatch:DescribeAlarms",
      "cloudwatch:EnableAlarmActions",
      "cloudwatch:DisableAlarmActions",
      "cloudwatch:DeleteAlarms"
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "sns:Subscribe",
      "sns:Publish"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name_prefix = "cloudwatch-policy-lullymorewest"
  policy      = data.aws_iam_policy_document.cloudwatch_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}



# resource "aws_iam_role_policy_attachment" "cloudwatch_policy" {
#   role          = aws_iam_role.cloudwatch_role.name
#   policy_arn    =  data.aws_iam_policy_document.cloudwatch_policy.arn
# }

#########################

#ORIGINAL

# permissions for logging, metrics and alarms 

# resource "aws_iam_policy_document" "cloudwatch_policy" {
#     name = "CloudWatchPolicy"
#     description = "Policy for CloudWatch logging, metrics and alarms"
#     policy = jsonencode({
#         Version = "2012-10-17"
#         Statement = [
#             {
#                 Effect = "Allow"
#                 Action = [
#                     "logs:CreateLogGroup",
#                     "logs:CreateLogStream",
#                     "logs:PutLogEvents",
#                     "logs:DescribeLogGroups",
#                     "logs:DescribeLogStreams",
#                     "logs:GetLogEvents",
#                     "logs:FilterLogEvents"
#                 ],
#                 "Resource": "*" 
#             },
#             {
#                 Effect = "Allow"
#                 Action = [
#                     "cloudwatch:PutMetricData",
#                     "cloudwatch:GetMetricStatistics",
#                     "cloudwatch:ListMetrics",
#                     "cloudwatch:ListMetricStreams",
#                     "cloudwatch:StartMetricStreams",
#                     "cloudwatch:StopMetricStreams",
#                     "cloudwatch:SetAlarmState",
#                     "cloudwatch:PutMetricAlarm",
#                     "cloudwatch:DescribeAlarms",
#                     "cloudwatch:EnableAlarmActions",
#                     "cloudwatch:DisableAlarmActions",
#                     "cloudwatch:DeleteAlarms"
#                 ],
#                 "Resource": "*"
#             },
#             {
#                 Effect = "Allow"
#                 Action = [
#                     "sns:Subscribe",
#                     "sns:Publish"
#                 ],
#                 "Resource": "*"
#             }
#         ]
#     }) 
# }

#JUST COMMENTING FOR THE PUSH