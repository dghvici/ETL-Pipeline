# Create the IAM policy document
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

# Create the IAM policy from the policy document
resource "aws_iam_policy" "cloudwatch_policy" {
  name        = "CloudWatchPolicy"
  description = "Policy for CloudWatch logging, metrics, and alarms"
  policy      = data.aws_iam_policy_document.cloudwatch_policy.json
}

# Create the IAM role for Lambda
resource "aws_iam_role" "cloudwatch_role" {
  name               = "cloudwatch-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach the IAM policy to the role
resource "aws_iam_role_policy_attachment" "cloudwatch_policy_attachment" {
  role       = aws_iam_role.cloudwatch_role.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}