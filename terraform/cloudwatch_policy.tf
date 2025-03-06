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

resource "aws_iam_role" "cloudwatch_role" {
    name    = "cloudwatch-role"
    assume_role_policy = data.aws_iam_policy.cloudwatch_policy.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_policy" {
  role          = aws_iam_role.cloudwatch_role.name
  policy_arn    =  data.aws_iam_policy_document.cloudwatch_policy.arn
}