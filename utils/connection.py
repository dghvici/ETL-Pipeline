import psycopg2
import logging
from dotenv import load_dotenv
import os


load_dotenv()

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
        return connection
    except Exception as error:
        logger.error(f"Error connecting to RDS: {error}")
        if raise_exception:
            raise error
        else:
            return None

def close_rds(conn):
    conn.close()
