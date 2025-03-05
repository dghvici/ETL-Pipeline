import logging 
import boto3
import os
from botocore.exceptions import ClientError

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm", "eu-west-2")

######################################################################
def get_last_imported_timestamp(): 
    try: 
        response = ssm.get_parameter(Name="LastImportedTimeStamp")
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        return None
    except ClientError as e: 
        logger.error(f"Error retriving the previous timestamp: {e}")
        raise e 

######################################################################    
def set_last_imported_timestamp(timestamp): 
    try: 
        ssm.put_parameter(
            Name="LastImportedTimeStamp",
            Value=timestamp,
            Type="String",
            Overwrite=True
        )
    except ClientError as e: 
        logger.error(f"Error setting LastImportedTimeStamp: {e}")
        raise e

