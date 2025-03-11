variable "ingest_lambda" {
  type    = string
  default = "Ingest-Lambda"
}

variable "transform_lambda" {
  type    = string
  default = "Transform-Lambda"
}

variable "load_lambda" {
  type    = string
  default = "Load-Lambda"
}

variable "default_timeout" {
  type    = number
  default = 120
}

variable "state_machine_name" {
  type    = string
  default = "Terrific-Totes-SNS"
}

#SecretManager Variables
variable "rds_user" {
  description = "The rds_user"
  type        = string
  sensitive   = true
  default     = "default"
}

variable "rds_password" {
  description = "The rds_password"
  type        = string
  sensitive   = true
  default     = "default"
}

variable "rds_host" {
  description = "The rds_host"
  type        = string
  sensitive   = true
  default     = "default"
}

variable "port" {
  description = "The rds port number"
  type        = string
  sensitive   = true
  default     = "default"
}

variable "rds_name" {
  description = "The rds name"
  type        = string
  sensitive   = true
  default     = "default"
}