# https://registry.terraform.io/providers/hashicorp/aws/latest/docs


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-2"

  default_tags {
    tags = { ProjectName = "De-terrific-totes-lullymore-west"
    DeployedFrom = "terraform"
    Repository = "NC-DATAENG-ETL-PROJECT"
    }
  }
}