import boto3
import json


def lambda_handler_transform(event, context):
    s3_client = boto3.client("s3")
    key = "test"
    bucket = "etl-lullymore-west-transformed"
    body = json.dumps(event)
    print(event)
    s3_client.put_object(Bucket=bucket, Key=key, Body=body)
    return True
