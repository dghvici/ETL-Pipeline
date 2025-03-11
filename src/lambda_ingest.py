import os
# import sys
import boto3

import json
# from dotenv import load_dotenv
import logging
import pytz
from datetime import datetime

from botocore.exceptions import ClientError
from util_func.python.connection import connect_to_rds, close_rds


# Set this environment variable before running the script locally
os.environ['ENV'] = 'local'  # or 'production' for Lambda

if os.getenv("ENV") == "development":
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import connect_to_rds, close_rds
from ingest_utils import (
    check_database_updated,
    retrieve_parameter,
    put_prev_time,
)

# else:
#     sys.path.append(
#         os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     )
# from util_func.python.connection import connect_to_rds, close_rds
# from util_func.python.ingest_utils import (
#     check_database_updated,
#     retrieve_parameter,
# )

ssm = boto3.client("ssm", "eu-west-2")

# load env variables
# load_dotenv()  # conditional only happens if runs in test environment

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# trigered by the state machine every 30min
def lambda_handler_ingest(event, context):
    try:
        conn = connect_to_rds()
        cur = conn.cursor()
        updated_data_tables = check_database_updated()
        previous_time = retrieve_parameter(ssm, "timestamp_prev")
        print(previous_time, "prev in lambda_handler")
        current_time = retrieve_parameter(ssm, "timestamp_now")
        print(current_time, "current in lambda_handler")
        if updated_data_tables == []:
            logger.info("No new data.")
        else:
            formatted_output_list = []
            for table in updated_data_tables:
                query = f"""SELECT * FROM {table}
                        WHERE last_updated BETWEEN '{previous_time}'
                        and '{current_time}';"""
                cur.execute(query)
                row_data = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                formatted_output = {
                    table: {"column_names": column_names, "rows": row_data}
                }
                formatted_output_list.append(formatted_output)
            formatted_output = {"New_data": formatted_output_list}
            json_body = json.dumps(formatted_output, default=str)
            s3_client = boto3.client("s3")
            year = datetime.now().year
            month = datetime.now().month
            key = f"{year}/{month}/totesys-data-ingested-{current_time}"
            bucket = "etl-lullymore-west-ingested"
            s3_client.put_object(Bucket=bucket, Key=key, Body=json_body)
            logger.info("All data has been ingested.")
        put_prev_time(ssm, str(current_time))
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception("An unexpected error occurred") from e
    finally:
        close_rds(conn)

