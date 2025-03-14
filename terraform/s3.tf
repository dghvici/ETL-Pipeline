resource "aws_s3_bucket" "ingestion_bucket" {
  bucket  = "lullymore-west-ingested-2025"
  tags = {
    Name = "BucketForDataIngestion"
  }
}

resource "aws_s3_bucket_notification" "ingestion_notification" {
  bucket = aws_s3_bucket.ingestion_bucket.id
  eventbridge = true
}

resource "aws_s3_bucket" "transform_bucket" {

  bucket = "lullymore-west-transformed-2025"
  tags = {
    Name = "BucketForDataTransformation"
  }
}

resource "aws_s3_bucket_notification" "transform_bucket_notification" {
  bucket = aws_s3_bucket.transform_bucket.id
  eventbridge = true
}
