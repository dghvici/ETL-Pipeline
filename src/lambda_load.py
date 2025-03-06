import boto3
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO
from sqlalchemy import create_engine
# import re
import logging
from botocore.exceptions import ClientError
import os
from utils.transform_load_utils import get_table_name

s3_client = boto3.client("s3")

#rds database credentials - needs updating based on github secrets/aws secrets
user=os.getenv("OLAP_USER")
password=os.getenv("OLAP_PASSWORD")
database=os.getenv("OLAP_NAME")
host=os.getenv("OLAP_HOST")
port=os.getenv("OLAP_PORT")

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler_load(event, context):
    """uploads data to the data warehouse, based on data uploaded
    to the transformed s3 bucket (saved in parquet format).

    Args:
        event: s3 event message in JSON format, containing a record of the
        objects put into the transformed s3 bucket during the
        lambda_handler_transform run
        context: supplied by AWS
    """
    # do not change lambda handler name --> linked to tf lamda handler resource
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        object_keys = [record["s3"]["object"]["key"] for record in event["Records"]]
        #loop through each object (e.g. parquet file)
        for object_key in object_keys:
            #retrieve the name of the table to be uploaded to from the key
            #assume key in format "2025/1/transformed-fact_sales_order-2025-01-02 24:09:04:3424"
            table_name = get_table_name(object_key)
            #load object from s3 bucket
            file_object = s3_client.get_object(Bucket=bucket, Key=object_key)
            #read as a parquet file
            parquet_file = pq.ParquetFile(BytesIO(file_object["Body"].read()))
            #load into a pandas dataframe
            df = parquet_file.read().to_pandas()
            #connect to RDS database
            #write each dataframe to RDS, based on if its a fact or dim table
            #use sqlalchemy (more straightforward than only psycopg2)
            connection_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
            engine = create_engine(connection_uri)
            if "fact" in table_name:
                df.to_sql(table_name, engine, if_exists="append", index=False)
            else:
                df.to_sql(table_name, engine, if_exists="append", index=False)
            #close connection
        logger.info("All data has been loaded into data warehouse.")
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception("An unexpected error occurred") from e
