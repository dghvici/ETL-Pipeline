# https://developer.hashicorp.com/terraform/language/values/variables

variable "ingest_lambda" {
  type    = string
  default = "ingest"
}

variable "transform_lambda" {
  type    = string
  default = "transform"
}

variable "load_lambda" {
  type    = string
  default = "load"
}

variable "default_timeout" {
  type    = number
  default = 10
}

variable "state_machine_name" {
  type    = string
  default = "terrific-totes-"
}

variable "S3_BUCKET_PREFIX" {
  type = string
}