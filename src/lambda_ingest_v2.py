import os
# import sys
import boto3
import json
from dotenv import load_dotenv
import logging
import pytz
from datetime import datetime
import pymysql 
from botocore.exceptions import ClientError
from util_func.python.connection import connect_to_rds, close_rds

 # Initialize Boto3 clients
secretsmanager = boto3.client("secretsmanager", "eu-west-2")
ssm = boto3.client("ssm", "eu-west-2")
s3_client = boto3.client("s3")
load_dotenv()  # conditional only happens if runs in test environment

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)