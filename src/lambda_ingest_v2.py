import os
# import sys
import boto3
import json
from dotenv import load_dotenv
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from util_func.python.connection import connect_to_rds, close_rds
from util_func.python.timestamps import get_last_imported_timestamp, set_last_imported_timestamp

 # Initialize Boto3 clients
secretsmanager = boto3.client("secretsmanager", "eu-west-2")
ssm = boto3.client("ssm", "eu-west-2")
s3_client = boto3.client("s3")
load_dotenv()  # local testing only

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler_ingest(event, context):
    try:
         # rds connection
        conn = connect_to_rds()
        cur = conn.cursor()

        # get last timestamp updates
        last_imported_timestamp = get_last_imported_timestamp()
        if last_imported_timestamp:
            # Incremental import: Import only new data
            fact_query = f"SELECT * FROM transactions WHERE updated_at > '{last_imported_timestamp}'"
            # other tables to go here

        # inital download 
        else: 
            fact_query = f"SELECT * FROM transactions;"
        
        cur.execute(fact_query)
        fact_data = cur.fetchall()

        # logger 
        logger.info(f"")

        # Upload data to S3 - could this be a util? 
        current_time = datetime().strftime('%Y-%m-%dT%H:%M:%SZ')
        for table, data in [("fact_table", fact_data)]:
            body = json.dumps(data)
            key = f"{datetime.now().year}/{datetime.now().month}/ingested-{table}-{current_time}.json"
            bucket = "etl-lullymore-west-ingested"
            s3_client.put_object(Bucket=bucket, Key=key, Body=body)

        # update timestamp 
        set_last_imported_timestamp(current_time)
        logger.info(f"last imported timestamp updated to {current_time}")

        # close rds 
        close_rds(conn)

        # return status code 
        return {
            'statusCode': 200,
            'body': json.dumps("Data retrieved successfully")
        }
    except ClientError as e: 
        logger.error(f"ClientError: {e}")
        return {
            'statusCode': 500
        }