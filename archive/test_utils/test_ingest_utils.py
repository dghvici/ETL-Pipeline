import boto3
import os
import pytz
import pytest
from datetime import datetime
from unittest.mock import patch
from moto import mock_aws
from utils.python.ingest_utils import (
    put_current_time,
    retrieve_parameter,
    put_prev_time,
    format_raw_data_into_json,
    check_database_updated,
)


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


class TestPutPrevTime:
    @mock_aws
    def test_put_prev_time_stores_parameter_in_parameter_store(self):
        # Arranging Mock SSM Client
        # with mock_aws():
        test_value = "2021-07-27T16:02:08.070557"
        ssm_client = boto3.client("ssm", "eu-west-2")

        # Inserting prev_time into parameter store
        put_prev_time(ssm_client, test_value)
        response = ssm_client.get_parameters(Names=["timestamp_prev"])
        assert response["Parameters"][0]["Value"] == test_value

    def test_stores_date_parameter_in_parameter_store(self, ssm_client):
        tz = pytz.timezone("Europe/London")
        timestamp_prev = tz.localize(
            datetime(2001, 12, 1, 0, 0, 0)
        ).isoformat()
        put_prev_time(ssm_client, timestamp_prev)
        response = ssm_client.get_parameter(Name="timestamp_prev")
        assert response["Parameter"]["Value"] == timestamp_prev

    def test_stores_time_and_date_parameter_in_parameter_store(
        self, ssm_client
    ):
        tz = pytz.timezone("Europe/London")
        timestamp_prev = tz.localize(datetime(2001, 12, 1, 1, 1)).isoformat()
        put_prev_time(ssm_client, timestamp_prev)
        response = ssm_client.get_parameter(Name="timestamp_prev")
        assert response["Parameter"]["Value"] == timestamp_prev

    def test_raises_value_error_for_invalid_date_format(self, ssm_client):
        invalid_timestamp = "2001-12-01T25:01:00"
        with pytest.raises(ValueError):
            put_prev_time(ssm_client, invalid_timestamp)


class TestPutCurrTime:
    @mock_aws
    def test_put_curr_time_stores_parameter_in_parameter_store(self):
        test_value = "2021-07-27T16:02:08.070557"
        ssm_client = boto3.client("ssm", "eu-west-2")
        put_current_time(ssm_client, test_value)
        response = ssm_client.get_parameters(Names=["timestamp_now"])
        assert response["Parameters"][0]["Value"] == test_value

    def test_stores_date_parameter_in_parameter_store(self, ssm_client):
        tz = pytz.timezone("Europe/London")
        timestamp_now = tz.localize(
            datetime(2003, 12, 17, 0, 0, 0)
        ).isoformat()
        put_current_time(ssm_client, timestamp_now)
        response = ssm_client.get_parameter(Name="timestamp_now")
        assert response["Parameter"]["Value"] == timestamp_now

    def test_stores_date_and_time_parameter_in_parameter_store(
        self, ssm_client
    ):
        tz = pytz.timezone("Europe/London")
        timestamp_now = tz.localize(
            datetime(2003, 12, 17, 2, 30, 0)
        ).isoformat()
        put_current_time(ssm_client, timestamp_now)
        response = ssm_client.get_parameter(Name="timestamp_now")
        assert response["Parameter"]["Value"] == timestamp_now

    def test_raises_value_error_for_invalid_time(self, ssm_client):
        invalid_timestamp = "2003-12-01T25:01:00"
        with pytest.raises(ValueError):
            put_current_time(ssm_client, invalid_timestamp)


class TestRetreieveParameter:
    @mock_aws
    def test_retreieve_param_retrieves_param_and_returns_string(self):
        ssm_client = boto3.client("ssm", "eu-west-2")
        parameter_name = "test_param"
        ssm_client.put_parameter(
            Name=parameter_name,
            Value="test_value",
            Type="String",
            Overwrite=True,
        )
        response = retrieve_parameter(ssm_client, parameter_name)
        assert response == "test_value"

    @mock_aws
    def test_get_param_raises_indexerror_if_name_doesnt_exist(self):
        ssm_client = boto3.client("ssm", "eu-west-2")
        parameter_name = "test_param"
        with pytest.raises(IndexError):
            retrieve_parameter(ssm_client, parameter_name)


class TestFormatter:
    def test_formatter(self):
        rows = [
            (
                18336,
                "SALE",
                12979,
                None,
                datetime(2025, 3, 5, 11, 6, 10, 363000),
            )
        ]
        column_names = ["col", "col1", "col2", "col3", "col4", "col5"]
        table_name = "test_table"
        response = format_raw_data_into_json(table_name, column_names, rows)
        assert response


class TestCheckDatabaseUpdated:
    @patch(
        "utils.python.ingest_utils.retrieve_parameter",
        side_effect=IndexError,
    )
    def test_check_db_updated_returns_all_tables_on_first_invokation(
        self, mock_retrieve_parameter
    ):
        response = check_database_updated()

        all_tables = [
            "transaction",
            "design",
            "sales_order",
            "address",
            "counterparty",
            "payment",
            "payment_type",
            "currency",
            "staff",
            "department",
            "purchase_order",
        ]

        assert response == all_tables

    @patch("utils.python.ingest_utils.connect_to_rds")
    @patch("utils.python.ingest_utils.retrieve_parameter")
    @patch("utils.python.ingest_utils.put_current_time")
    @patch("utils.python.ingest_utils.put_prev_time")
    def test_check_database_updated_no_updates(
        self,
        mock_put_prev_time,
        mock_put_current_time,
        mock_retrieve_parameter,
        mock_connect_to_rds,
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_put_prev_time.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [],  # transaction
            [],  # design
            [],  # sales_order
            [],  # address
            [],  # counterparty
            [],  # payment
            [],  # payment_type
            [],  # currency
            [],  # staff
            [],  # department
            [],  # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == []
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()

    @patch("utils.python.ingest_utils.connect_to_rds")
    @patch("utils.python.ingest_utils.retrieve_parameter")
    @patch("utils.python.ingest_utils.put_current_time")
    @patch("utils.python.ingest_utils.put_prev_time")
    def test_check_database_updated_one_table(
        self,
        mock_put_prev_time,
        mock_put_current_time,
        mock_retrieve_parameter,
        mock_connect_to_rds,
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_put_prev_time.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [("2003-12-17T00:00:00",)],  # transaction
            [],  # design
            [],  # sales_order
            [],  # address
            [],  # counterparty
            [],  # payment
            [],  # payment_type
            [],  # currency
            [],  # staff
            [],  # department
            [],  # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == ["transaction"]
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()

    @patch("utils.python.ingest_utils.connect_to_rds")
    @patch("utils.python.ingest_utils.retrieve_parameter")
    @patch("utils.python.ingest_utils.put_current_time")
    @patch("utils.python.ingest_utils.put_prev_time")
    def test_check_database_updated_multiple_tables(
        self,
        mock_put_prev_time,
        mock_put_current_time,
        mock_retrieve_parameter,
        mock_connect_to_rds,
    ):
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
        mock_conn = mock_connect_to_rds.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [("2003-12-17T00:00:00",)],  # transaction
            [],  # design
            [],  # sales_order
            [],  # address
            [],  # counterparty
            [],  # payment
            [
                ("2003-12-17T00:00:00"),
            ],  # payment_type
            [],  # currency
            [],  # staff
            [("2003-12-17T00:00:00",)],  # department
            [],  # purchase_order
        ]
        updated_tables = check_database_updated()
        assert updated_tables == ["transaction", "payment_type", "department"]
        mock_cursor.execute.assert_called()
        mock_cursor.fetchall.assert_called()
        mock_put_current_time.assert_called()
