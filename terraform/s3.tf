resource "aws_s3_bucket" "ingestion_bucket" {
  bucket  = "etl-lullymore-west-ingested"
  tags = {
    Name = "BucketForDataIngestion"
  }
}

resource "aws_s3_bucket" "transform_bucket" {

  bucket = "etl-lullymore-west-transformed"
  tags = {
    Name = "BucketForDataTransformation"
  }
}

