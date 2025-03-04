import os
import psycopg2
from dotenv import load_dotenv
import logging

# load env variables
load_dotenv()  # conditional only happens if runs in test environment

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        logger.info(os.getenv("RDS_NAME"))
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


# TO BE DELETED
###############################################################################


# def execute_query(query, params=None):
#     conn = connect_to_rds()
#     if conn is None:
#         logger.error("Failed to connect to RDS")
#         return None

#     try:
#         cursor = conn.cursor()
#         cursor.execute(query, params)
#         results = cursor.fetchall()
#         cursor.close()
#         return results
#     except Exception as error:
#         logger.error(f"Error executing query: {error}")
#         return None
#     finally:
#         close_rds(conn)


###############################################################################


def close_rds(conn):
    if conn is not None:
        conn.close()
        logger.info("Connection to RDS closed")
    else:
        logger.error("Connection to RDS is already closed")
