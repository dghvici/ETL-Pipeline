import re
import boto3
import pyarrow.parquet as pq
from io import BytesIO
import logging

s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_table_name(file_key):
    """function to extract the table name from the
    filenames"""
    try:
        if "ingested" in file_key:
            re_pattern = r"ingested-(\w+)"
        elif "transformed" in file_key:
            re_pattern = r"transformed-(\w+)"

        match = re.search(re_pattern, file_key)
        table_name = match.group(1)
        return table_name
    except UnboundLocalError as e:
        logger.error("File name does not conform to the expected \
        format (does not include 'ingested' or 'transformed')")
        raise


