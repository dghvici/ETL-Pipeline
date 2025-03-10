# import boto3
# from util_func.python.ingest_utils import (
#     put_current_time,
#     retrieve_parameter,
#     put_prev_time,
#     format_raw_data_into_json
# )
# from moto import mock_aws
# import datetime

# # from unittest.mock import patch
# import os
# import pytest


# @pytest.fixture(scope="function")
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# class TestPutPrevTime:
#     @mock_aws
#     def test_put_prev_time_stores_parameter_in_parameter_store(self):
#         # Arranging Mock SSM Client
#         # with mock_aws():
#         test_value = "test"
#         ssm_client = boto3.client("ssm", "eu-west-2")

#         # Inserting prev_time into parameter store
#         put_prev_time(ssm_client, test_value)
#         response = ssm_client.get_parameters(Names=["timestamp_prev"])
#         assert response["Parameters"][0]["Value"] == test_value


# class TestPutCurrTime:
#     @mock_aws
#     def test_put_curr_time_stores_parameter_in_parameter_store(self):
#         test_value = "test"
#         ssm_client = boto3.client("ssm", "eu-west-2")
#         put_current_time(ssm_client, test_value)
#         response = ssm_client.get_parameters(Names=["timestamp_now"])
#         assert response["Parameters"][0]["Value"] == test_value


# class TestRetreieveParameter:
#     @mock_aws
#     def test_retreieve_param_retrieves_param_and_returns_string(self):
#         ssm_client = boto3.client("ssm", "eu-west-2")
#         parameter_name = "test_param"
#         ssm_client.put_parameter(
#             Name=parameter_name,
#             Value="test_value",
#             Type="String",
#             Overwrite=True,
#         )
#         response = retrieve_parameter(ssm_client, parameter_name)
#         assert response == "test_value"

#     @mock_aws
#     def test_get_param_raises_indexerror_if_name_doesnt_exist(self):
#         ssm_client = boto3.client("ssm", "eu-west-2")
#         parameter_name = "test_param"
#         with pytest.raises(IndexError):
#             retrieve_parameter(ssm_client, parameter_name)


# # class TestCheckDatabaseUpdated:
# #     @patch(
# #         "util_func.python.ingest_utils.retrieve_parameter",
# #         side_effect=IndexError,
# #     )
# #     def test_check_db_updated_returns_all_tables_on_first_invokation(
# #         self, mock_retrieve_parameter
# #     ):
# #         check_database_updated()

# #     all_tables = [
# #         "transaction",
# #         "design",
# #         "sales_order",
# #         "address",
# #         "counterparty",
# #         "payment",
# #         "payment_type",
# #         "currency",
# #         "staff",
# #         "department",
# #         "purchase_order",
# #     ]

# #     assert response == all_tables


# class TestFormatter:
#     def test_formatter(self):
#         rows = [
#             (18336,
#              'SALE',
#              12979,
#              None,
#              datetime.datetime(2025, 3, 5, 11, 6, 10, 363000))
#         ]
#         column_names = ["col", "col1", "col2", "col3", "col4", "col5"]
#         table_name = "test_table"
#         response = format_raw_data_into_json(table_name, column_names, rows)
#         assert response
