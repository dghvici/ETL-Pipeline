resource "aws_s3_bucket" "ingestion_bucket" {
  bucket  = "lullymore-west-ingested-2025"
  tags = {
    Name = "BucketForDataIngestion"
  }
}

resource "aws_s3_bucket" "transform_bucket" {

  bucket = "lullymore-west-transformed-2025"
  tags = {
    Name = "BucketForDataTransformation"
  }
}

