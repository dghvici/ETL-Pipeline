#http://docs.getmoto.org/en/latest/docs/getting_started.html


from src.lambda_ingest import lambda_handler_ingest
from moto import mock_aws
import boto3
import pytest
import os
from utils.connection import connect_to_rds

@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    os.environ ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ ["AWS_SESSION_TOKEN"] = "testing"
    os.environ ["AWS_DEFAULT _REGION"] = "eu-west-2"

class TestIngest():

    def test_ingests_all_data_with_empty_db(self, aws_credentials):
        # mock db 
        # mock connection
        # ingest mock db
        # assert result is null

        with mock_aws():
            rdsdata = boto3.client("rds", region_name="eu-west-2")
            conn = connect_to_rds()
            event = "event"
            context = "context"
            response = lambda_handler_ingest(event, context)
            # resp = rdsdata.execute_statement(resourceArn="not applicable", secretArn="not applicable", sql="SELECT some FROM thing")
            assert response == "No new data."

    def test_connection_ingests_all_data(self):
        conn = connect_to_rds()
        cur = conn.cursor()
        query = """SELECT * FROM currency"""
        cur.execute(query)
        event = "event"
        context = "context"
        response = lambda_handler_ingest(event, context)
        assert response == "All data has been ingested."


        # connect to local db 
        # NB:create local database connection
        # ingest mock db
        # assert result is everything in mock db



    def test_if_no_updates_in_db_no_ingestion_needed(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1= ingest mock db
        # result_2= ingest mock db (capture message --> No new data)
        # assert result_1 == result_2
        # assert response(results_2) == No new data
        pass

    def test_if_updates_in_db_ingested(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1= ingest mock db
        # result_2= ingest mock db (capture message --> No new data)
        # assert result_1 == result_2
        # assert response(results_2) == No new data
        pass

    def test_that_file_successfuly_uploaded_to_s3(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1 = ingest mock db
        # list s3 objects
        # assert result_1 json file name in list s3 object
        pass

    def test_that_data_is_immutable_in_s3(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1 = ingest mock db
        # update db
        # first_ingest_list = list s3 objects
        # result_2 = ingest mock bd
        # second_ingest_list = list s3 objects
        # assert first_ingest != second_ingest
        pass