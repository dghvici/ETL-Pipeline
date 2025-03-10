import boto3
import os
import pytest
from moto import mock_aws
from unittest.mock import patch
# from datetime import datetime
from util_func.python.ingest_utils import (
    retrieve_parameter, check_database_updated
)
from util_func.python.connection import connect_to_rds, close_rds

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function")
def ssm_client(aws_credentials):
    with mock_aws():
        yield boto3.client("ssm", region_name="eu-west-2")

class TestRetrieveParameter:
    def test_retreieve_param_retrieves_param_and_returns_string(
        self, ssm_client):
        parameter_name = "test_param"
        ssm_client.put_parameter(
            Name=parameter_name,
            Value="test_value",
            Type="String",
            Overwrite=True,
        )
        response = retrieve_parameter(ssm_client, parameter_name)
        assert response == "test_value"

    def test_get_param_raises_indexerror_if_name_doesnt_exist(
        self, ssm_client):
        with pytest.raises(IndexError):
            retrieve_parameter(ssm_client, "non_existent_param")


class TestCheckDatabaseUpdated:
    @patch("util_func.python.ingest_utils.connect_to_rds")
    @patch("util_func.python.ingest_utils.retrieve_parameter")
    @patch("util_func.python.ingest_utils.put_current_time")
    @patch("util_func.python.ingest_utils.put_prev_time")
    def test_check_database_updated_no_updates(
        self, mock_put_prev_time, mock_put_current_time,
        mock_retrieve_parameter, mock_connect_to_rds
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [], # transaction
            [], # design
            [], # sales_order
            [], # address
            [], # counterparty
            [], # payment
            [], # payment_type
            [], # currency
            [], # staff
            [], # department
            [], # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == []
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()
        mock_put_prev_time.assert_called()

    @patch("util_func.python.ingest_utils.connect_to_rds")
    @patch("util_func.python.ingest_utils.retrieve_parameter")
    @patch("util_func.python.ingest_utils.put_current_time")
    @patch("util_func.python.ingest_utils.put_prev_time")
    def test_check_database_updated_one_table(
        self, mock_put_prev_time, mock_put_current_time,
        mock_retrieve_parameter, mock_connect_to_rds
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [("2003-12-17T00:00:00",)], # transaction
            [], # design
            [], # sales_order
            [], # address
            [], # counterparty
            [], # payment
            [], # payment_type
            [], # currency
            [], # staff
            [], # department
            [], # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == [
            "transaction"
            ]
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()
        mock_put_prev_time.assert_called()

    @patch("util_func.python.ingest_utils.connect_to_rds")
    @patch("util_func.python.ingest_utils.retrieve_parameter")
    @patch("util_func.python.ingest_utils.put_current_time")
    @patch("util_func.python.ingest_utils.put_prev_time")
    def test_check_database_updated_multiple_tables(
        self, mock_put_prev_time, mock_put_current_time,
        mock_retrieve_parameter, mock_connect_to_rds
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [("2003-12-17T00:00:00",)], # transaction
            [], # design
            [], # sales_order
            [], # address
            [], # counterparty
            [], # payment
            [("2003-12-17T00:00:00"),], # payment_type
            [], # currency
            [], # staff
            [("2003-12-17T00:00:00",)], # department
            [], # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == [
            "transaction", "payment_type", "department"
            ]
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()
        mock_put_prev_time.assert_called()