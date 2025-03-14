import os
import boto3
import psycopg2

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


def connect_to_rds(raise_exception=False):
    """connects to Totesys AWS Rational Database Service (RDS) database.
    Note: locally, credentials are supplied by product owner and stored
    locally in gitignored .env. For production, these credentials are
    stored in GitHub Secrets and passed to AWS Sectrets Manager, which
    are is used in place of the .env.

    Errors are logged and raised if there is an problem connecting
    to the database.

    Returns:
        connection: connection to totesys RDS database
    """
    try:
        connection = psycopg2.connect(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )
        logger.info("Successfully connected to RDS")
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


def close_rds(conn):
    """Function to close the connection to the RDS database. Logs an error if
    connection is already closed.

    Args:
        conn (connection): connection instance to the database.
    """
    if conn is not None:
        conn.close()
        logger.info("Connection to RDS closed")
    else:
        logger.error("Connection to RDS is already closed")


# Not Tested
# def get_secret(secret_name):
#     """Function to get a secret from the AWS Secrets Manager.

#     Raises an error if there is a problem retrieving the secret
#     (i.e. issue connecting to Secrets Manager or if secretId
#     incorrect).

#     Args:
#         secret_name (str): string representing the SecretId

#     Returns:
#         The value of the secret.
#     """
#     try:
#         response = secretsmanager.get_secret_value(SecretId=secret_name)
#         return json.loads(response["SecretString"])
#     except ClientError as e:
#         logger.error(f"Error retrieving secret {secret_name}: {e}")
#         raise e
