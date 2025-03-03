resource "aws_secretsmanager_secret" "rds_user" {
  #checkov:skip=CKV2_AWS_57: This variable does not need to be rotated
  name                    = "rds_user"
  recovery_window_in_days = 0
  kms_key_id              = aws_kms_key.local_key.id
}

resource "aws_secretsmanager_secret_version" "rds_user_version" {
  secret_id     = aws_secretsmanager_secret.rds_user.id
  secret_string = var.rds_user

  depends_on = [ aws_secretsmanager_secret.rds_password ]
  #The value is passed to the Terraform via the CLI
}

resource "aws_secretsmanager_secret" "rds_password" {
  #checkov:skip=CKV2_AWS_57: This variable does not need to be rotated
  name                    = "rds_password"
  recovery_window_in_days = 0
  kms_key_id              = aws_kms_key.local_key.id
}

resource "aws_secretsmanager_secret_version" "rds_password_version" {
  secret_id     = aws_secretsmanager_secret.rds_password.id
  secret_string = var.rds_password
  #The value is passed to the Terraform via the CLI
}

resource "aws_secretsmanager_secret" "rds_name" {
  #checkov:skip=CKV2_AWS_57: This variable does not need to be rotated
  name                    = "rds_name"
  recovery_window_in_days = 0
  kms_key_id              = aws_kms_key.local_key.id
}

resource "aws_secretsmanager_secret_version" "rds_name_version" {
  secret_id     = aws_secretsmanager_secret.rds_name.id
  secret_string = var.rds_name
  #The value is passed to the Terraform via the CLI
}


resource "aws_secretsmanager_secret" "rds_host" {
  #checkov:skip=CKV2_AWS_57: This variable does not need to be rotated
  name                    = "rds_host"
  recovery_window_in_days = 0
  kms_key_id              = aws_kms_key.local_key.id
}

resource "aws_secretsmanager_secret_version" "rds_host_version" {
  secret_id     = aws_secretsmanager_secret.rds_host.id
  secret_string = var.rds_host
  #The value is passed to the Terraform via the CLI
}

resource "aws_secretsmanager_secret" "port" {
  #checkov:skip=CKV2_AWS_57: This variable does not need to be rotated
  name                    = "port"
  recovery_window_in_days = 0
  kms_key_id              = aws_kms_key.local_key.id
}

resource "aws_secretsmanager_secret_version" "port_version" {
  secret_id     = aws_secretsmanager_secret.port.id
  secret_string = var.port
  #The value is passed to the Terraform via the CLI
}