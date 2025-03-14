
resource "aws_kms_key" "local_key" {
  description             = "KMS key for AWS Secrets Manager"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}
resource "aws_kms_alias" "key" {
  name          = "alias/secret-encryption"
  target_key_id = aws_kms_key.local_key.id
}
resource "aws_kms_key_policy" "encrypt_kms" {
  key_id = aws_kms_key.local_key.id
  policy = jsonencode({
    Id      = "encrypt-secretsmanager"
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow access through AWS Secrets Manager for all principals in the account that are authorized to use AWS Secrets Manager"
        Effect = "Allow"
        Principal = {
          AWS = ["*"]
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:CreateGrant",
          "kms:DescribeKey"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:CallerAccount" = "${data.aws_caller_identity.current.account_id}"
            "kms:ViaService"    = "secretsmanager.${data.aws_caller_identity.current.account_id}.amazonaws.com"
          }
        }
      },
      {
        Sid    = "Allow access through AWS Secrets Manager for all principals in the account that are authorized to use AWS Secrets Manager"
        Effect = "Allow"
        Principal = {
          AWS = ["*"]
        }
        Action   = "kms:GenerateDataKey*"
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:CallerAccount" = "${data.aws_caller_identity.current.account_id}"
          }
          StringLike = {
            "kms:ViaService" = "secretsmanager.${data.aws_caller_identity.current.account_id}.amazonaws.com"
          }
        }
      },
      {
        Sid    = "Allow direct access to key metadata to the account"
        Effect = "Allow"
        Principal = {
          AWS = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
        }
        Action = [
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
          "kms:RevokeGrant"
        ]
        Resource = "*"
      }
    ]
  })
}
