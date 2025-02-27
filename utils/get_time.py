import random
from pprint import pprint
import json
import boto3
from datetime import datetime

ssm = boto3.client("ssm", "eu-west-2")
def put_prev_time(ssm, timestamp_prev):
    response = ssm.put_parameter(
        Name="timestamp_prev",
        Description="Time database was last queried",
        Value=timestamp_prev,
        Type='String',
        Overwrite=True
    )

def put_current_time(ssm, timestamp_now):
    response = ssm.put_parameter(
        Name="timestamp_now",
        Description="Time database queried",
        Value=timestamp_now,
        Type='String',
        Overwrite=True
    )


def get_parameter(ssm, parameter_name, **kwargs):
  try:
    if parameter_name: 
      response = ssm.get_parameters(
          Names = [parameter_name]
      )

    #   for parameter in response['Parameters']:
    return response['Parameters'][0]['Value']
      
    
    # return None
  except Exception as err:
    return {
        'result': 'FAILURE',
        'message' : 'Not Found'
     }

pprint(put_prev_time(ssm,'1981-01-01 00:00:00.000'))
pprint(get_parameter(ssm, "timestamp_prev"))
  