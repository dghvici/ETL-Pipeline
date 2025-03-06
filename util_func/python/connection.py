import os, boto3, psycopg2
from botocore.exceptions import ClientError
import json 
from dotenv import load_dotenv
import logging

# Initialize Boto3 clients
secretsmanager = boto3.client("secretsmanager", "eu-west-2")
ssm = boto3.client("ssm", "eu-west-2")
s3_client = boto3.client("s3")

# load env variables
load_dotenv()

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


######################################################################
def connect_to_rds(raise_exception=False):
    try:
        connection = psycopg2.connect(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )
        logger.info("Successfully connected to RDS")
        # logger.info(os.getenv("RDS_NAME"))
        return connection
    except psycopg2.OperationalError as op_error:
        logger.error(f"OperationalError connecting to RDS: {op_error}")
        if raise_exception:
            raise
        return None
    except Exception as error:
        logger.error(f"Error connection to RDS: {error}")
        if raise_exception:
            raise
        return None

######################################################################
def close_rds(conn):
    if conn is not None:
        conn.close()
        logger.info("Connection to RDS closed")
    else:
        logger.error("Connection to RDS is already closed")

######################################################################
def get_secret(secret_name):
    try:
        response = secretsmanager.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        raise e
    
