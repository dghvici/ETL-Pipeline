import boto3
import json

def lambda_handler_ingest(event, context):
        # trigered by the state machine every 30min
        # check for updated data --> use util check_for updates
        # util returns table names of data that has been updated
        # for table in all returned table names
        # first instance --> ingest all data 
                # connect to database
                # fetch parameter from store: time previous and time now 
                # SELECT * FROM table WHER time.previous < time.now
                # extract last updated data 
                # Json dump to S3 --> make sure a new object is created all the time 
                        # s3_client = boto3.client("s3")
                        # body = json.dumps("requirements.txt") add timestamp to name
                        # key = "random_file"
                        # bucket = "lullymore-west-ingested"
                        # s3_client.put_object(Bucket=bucket, Key=key, Body=body)
        # consecutive runs ingest data that's been recently adaded 
        # TO CONSIDER
        # except ClientError
                # DB connection - considered already
                # check updated - considered already
                # parameter store error --> raise previously? 
                # write to s3 --> to be captured here
       
        return True

