import boto3
import psycopg2
import logging
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()

def connect_to_rds(): 

    user=os.getenv("PG_USER")
    password=os.getenv("PG_PASSWORD")
    database=os.getenv("DB_NAME")
    host=os.getenv("DB_HOST")
    port=os.getenv("PORT")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
         conn = psycopg2.connect(
            host=host, 
            user=user, 
            password=password, 
            database=database
            )
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)

    logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")
    print(conn)

    return conn
    
conn = connect_to_rds()
print(conn, '<<line 44')

def close_rds(conn):
    conn.close()