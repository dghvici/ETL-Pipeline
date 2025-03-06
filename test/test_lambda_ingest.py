# import pytest
# from unittest.mock import patch, Mock
# from src.lambda_ingest import lambda_handler_ingest
# from botocore.exceptions import ClientError
# #additional imports
# import boto3
# from moto import mock_aws
# import os

# #additional fixture
# @pytest.fixture(scope="function")
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

# class TestIngestion:

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_ingestion_with_no_new_data(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#         caplog,
#     ):
#         mock_check_database_updated.return_value = []
#         event = {}
#         context = {}
#         lambda_handler_ingest(event, context)
#         assert "No new data." in caplog.text
#         # assert lambda_handler_ingest(event, context) == "No new data."

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_connection_ingests_all_data(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#         caplog,
#     ):
#         mock_check_database_updated.return_value = ["transaction"]
#         mock_conn = Mock()
#         mock_cur = Mock()
#         mock_connect_to_rds.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchall.return_value = [{"id": 1, "data": "sample data"}]
#         mock_s3_client = Mock()
#         mock_boto_client.return_value = mock_s3_client
#         event = {}
#         context = {}
#         lambda_handler_ingest(event, context)
#         assert "All data has been ingested." in caplog.text

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_if_updates_in_db_ingested(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#     ):
#         mock_check_database_updated.return_value = ["transaction"]
#         mock_conn = Mock()
#         mock_cur = Mock()
#         mock_connect_to_rds.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchall.return_value = [{"id": 1, "data": "sample data"}]
#         mock_get_parameter.return_value = "timestamp_value"
#         event = {}
#         context = {}
#         lambda_handler_ingest(event, context)
#         assert mock_get_parameter.call_count == 2

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_that_file_successfully_uploaded_to_s3(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#     ):
#         mock_check_database_updated.return_value = ["transaction"]
#         mock_conn = Mock()
#         mock_cur = Mock()
#         mock_connect_to_rds.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchall.return_value = [
#             (
#                 1,
#                 "PURCHASE",
#                 1,
#                 1,
#                 "2022-11-03 14:20:52.186",
#                 "2022-11-03 14:20:52.186",
#             ),
#             (
#                 2,
#                 "SALE",
#                 2,
#                 2,
#                 "2022-11-22 17:02:10.130",
#                 "2022-11-22 17:02:10.130",
#             ),
#         ]
#         mock_s3_client = Mock()
#         mock_boto_client.return_value = mock_s3_client
#         event = {}
#         context = {}
#         lambda_handler_ingest(event, context)
#         assert mock_s3_client.put_object.call_count == 1

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_connection_closed_after_ingestion(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#     ):
#         mock_check_database_updated.return_value = ["transaction"]
#         mock_conn = Mock()
#         mock_cur = Mock()
#         mock_connect_to_rds.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchall.return_value = [
#             (
#                 1,
#                 "PURCHASE",
#                 1,
#                 1,
#                 "2022-11-03 14:20:52.186",
#                 "2022-11-03 14:20:52.186",
#             ),
#             (
#                 2,
#                 "SALE",
#                 2,
#                 2,
#                 "2022-11-22 17:02:10.130",
#                 "2022-11-22 17:02:10.130",
#             ),
#         ]
#         event = {}
#         context = {}
#         lambda_handler_ingest(event, context)
#         assert mock_conn.close.call_count == 1

#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     def test_client_error(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#     ):
#         mock_check_database_updated.side_effect = ClientError(
#             {"Error": {"Code": "DB connection error"}}, "DB connection error"
#         )
#         event = {}
#         context = {}
#         with pytest.raises(
#             Exception,
#             match="Error interacting with AWS services",
#         ):
#             lambda_handler_ingest(event, context)


#additional tests - currently do not work because struggling to patch/mock the 
#output of the cur.description/column names
# class TestIngestionAdditional:
#     @patch("src.lambda_ingest.check_database_updated")
#     @patch("src.lambda_ingest.connect_to_rds")
#     @patch("src.lambda_ingest.retrieve_parameter")
#     @patch("src.lambda_ingest.boto3.client")
#     @patch("src.lambda_ingest.lambda_handler_ingest.column_names", return_value=["col1", "col2"])
#     def test_data_uploaded_to_s3_bucket(
#         self,
#         mock_boto_client,
#         mock_get_parameter,
#         mock_connect_to_rds,
#         mock_check_database_updated,
#         aws_credentials
#     ):
#         with mock_aws():
#             mock_check_database_updated.return_value = ["transaction"]
#             mock_conn = Mock()
#             mock_cur = Mock()
#             mock_connect_to_rds.return_value = mock_conn
#             mock_conn.cursor.return_value = mock_cur
#             mock_cur.fetchall.return_value = [("d", "c"), ("a", "b")]
            
#             #added the mock_cur.description return val
#             mock_get_parameter.return_value = "timestamp_value"
#             event = {}
#             context = {}

#             bucket_name = "lullymore-west-ingested"
#             s3_client = boto3.client("s3")

#             lambda_handler_ingest(event, context)

#             objects = s3_client.list_objects_v2(Bucket=bucket_name)
#             obj_keys = [obj["Key"] for obj in objects["Contents"]]
#             assert "ingested-transaction" in obj_keys[0]

    # @patch("src.lambda_ingest.check_database_updated")
    # @patch("src.lambda_ingest.connect_to_rds")
    # @patch("src.lambda_ingest.retrieve_parameter")
    # @patch("src.lambda_ingest.boto3.client")
    # def test_one_datafile_uploaded_to_s3_with_suitable_content(
    #     self,
    #     mock_boto_client,
    #     mock_get_parameter,
    #     mock_connect_to_rds,
    #     mock_check_database_updated,
    #     aws_credentials
    # ):
    #     with mock_aws():
    #         mock_check_database_updated.return_value = ["transaction"]
    #         mock_conn = Mock()
    #         mock_cur = Mock()
    #         mock_connect_to_rds.return_value = mock_conn
    #         mock_conn.cursor.return_value = mock_cur
    #         mock_cur.fetchall.return_value = [("d", "c"), ("a", "b")]
            
    #         #added the mock_cur.description return val
    #         mock_cur.description.return_value = [
    #             ("test_col1", 4, 12, 10, 1, None, None), 
    #             ("test_col2", 2, 13, 10, 1, None, None)]
    #         mock_get_parameter.return_value = "timestamp_value"
    #         event = {}
    #         context = {}
    #         expected_body = {
    #             "transaction": 
    #                 {"column_names": ["test_col1", "test_col2"]},
    #                 "rows": [("d", "c"), ("a", "b")]}
    #         bucket_name = "lullymore-west-ingested"
    #         s3_client = boto3.client("s3")

    #         lambda_handler_ingest(event, context)

    #         objects = s3_client.list_objects_v2(Bucket=bucket_name)
    #         obj_keys = [obj["Key"] for obj in objects["Contents"]]
    #         response = s3_client.get_object(Bucket=bucket_name, Key=obj_keys[0])

    #         assert response["Body"].read().decode("utf-8") == expected_body