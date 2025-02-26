# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket


resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "lullymore-west-ingested"
  tags = {
    Name = "BucketForDataIngestion"
  }
}


resource "aws_s3_bucket" "transform_bucket" {

  bucket = "lullymore-west-transformed"
  tags = {
    Name = "BucketForDataTransformation"
  }
}

# data "aws_iam_policy_document" "s3_document" {
#   statement {
#     actions = ["s3:PutObject"]
#     resources = [
#       "${aws_s3_bucket.ingestion_bucket.arn}/*",
#       "${aws_s3_bucket.transform_bucket.arn}/*",
#     ]
#   }
# }


# resource "aws_iam_policy" "s3_policy" {
#   name_prefix = "s3-policy-terrific-totes-lambda-"
#   policy      = data.aws_iam_policy_document.s3_document.json
# }


## Copied from docs, will need to be populated once lambda iam role is created.
# resource "aws_iam_policy_attachment" "test-attach" {
#   name       = "test-attachment"
#   users      = [aws_iam_user.user.name]
#   roles      = [aws_iam_role.role.name]
#   groups     = [aws_iam_group.group.name]
#   policy_arn = aws_iam_policy.policy.arn
# }