import boto3
import json
from utils.ingest_utils import check_database_updated, get_parameter
from utils.connection import connect_to_rds, close_rds
from datetime import datetime
from botocore.exceptions import ClientError


ssm = boto3.client("ssm", "eu-west-2")


# trigered by the state machine every 30min
def lambda_handler_ingest(event, context):
        try:
            updated_data_tables = check_database_updated()
            if updated_data_tables == []:
                  return "No new data."
            else:
                for table in updated_data_tables:
                        conn = connect_to_rds()
                        cur = conn.cursor()
                        previous_time = get_parameter(ssm, "timestamp_prev")
                        current_time = get_parameter(ssm, "timestamp_now")
                        query = f"""SELECT * FROM {table} 
                        WHERE last_updated BETWEEN '{previous_time}' and '{current_time}';"""
                        response = cur.execute(query)
                        close_rds(conn)
                        s3_client = boto3.client("s3")
                        body = json.dumps(response) 
                        key = f"ingested{datetime.now()}"
                        bucket = "lullymore-west-ingested"
                        s3_client.put_object(Bucket=bucket, Key=key, Body=body)
                return "All data has been ingested."
        # consecutive runs ingest data that's been recently adaded 
        # TO CONSIDER
        except ClientError as e:
                # DB connection - considered already
                if e =="DB conn":
                      raise "Can't connect to DataBase"
                # check updated - considered already
                # parameter store error --> raise previously? 
                # write to s3 --> to be captured here


