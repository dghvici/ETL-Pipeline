# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
#import json
#import boto3





def lambda_handler_transform(event, context):

# Load json data from bucket (json.loads - unsure if needed to transform json data, as ingestion phase ingests as dict of tuples)
# import boto3
# import json

# s3 = boto3.resource('s3')

# content_object = s3.Object('test', 'sample_json.txt')
# file_content = content_object.get()['Body'].read().decode('utf-8')
# json_content = json.loads(file_content)
# print(json_content['Details'])
#transform json data to DF
#Convert DF to pyarrow table
#output as parquet
#Load this to the transformation bucket




# placeholder for the purpose of the CICD pipeline
# do not change lambda handler name --> linked to tf lamda handler resource

#Import


    return True
