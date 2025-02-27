# https://developer.hashicorp.com/terraform/language/values/variables

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
  default = 10
}

variable "state_machine_name" {
  type    = string
  default = "Terrific-Totes-SNS"
}

# variable "S3_BUCKET_PREFIX" {
#   type = string
# }