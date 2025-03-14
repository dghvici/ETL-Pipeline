import pytest
import os
import psycopg2
import pytz
from moto import mock_aws
import boto3
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from botocore.exceptions import ClientError
from src.lambda_ingest import (
    lambda_handler_ingest,
    connect_to_rds,
    close_rds,
    put_current_time,
    put_prev_time,
    check_database_updated,
    format_raw_data_into_json,
    retrieve_parameter,
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


class TestIngestion:
    @mock_aws
    @patch("src.lambda_ingest.check_database_updated")
    @patch("src.lambda_ingest.connect_to_rds")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.boto3.client")
    @patch("src.lambda_ingest.put_prev_time")
    def test_ingestion_with_no_new_data(
        self,
        mock_put_prev_time,
        mock_boto_client,
        mock_get_parameter,
        mock_connect_to_rds,
        mock_check_database_updated,
        caplog,
    ):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect_to_rds.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        mock_get_parameter.return_value = "2021-07-27T16:02:08.070557"
        mock_check_database_updated.return_value = []
        mock_put_prev_time.return_value = None
        event = {}
        context = {}
        lambda_handler_ingest(event, context)
        assert "No new data." in caplog.text

    @mock_aws
    @patch("src.lambda_ingest.put_prev_time")
    @patch("src.lambda_ingest.boto3.client")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.check_database_updated")
    @patch("src.lambda_ingest.connect_to_rds")
    def test_connection_ingests_all_data(
        self,
        mock_connect_to_rds,
        mock_check_database_updated,
        mock_get_parameter,
        mock_boto_client,
        mock_put_prev_time,
        caplog,
    ):
        mock_conn = MagicMock()
        mock_connect_to_rds.return_value = mock_conn
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        print(mock_cur)

        mock_check_database_updated.return_value = ["transaction"]
        mock_get_parameter.return_value = "2021-07-27T16:02:08.070557"
        mock_cur.fetchall.return_value = [{"id": 1, "data": "sample data"}]
        mock_cur.description = [("col1",), ("col2",)]

        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        mock_put_prev_time.return_value = None
        event = {}
        context = {}
        lambda_handler_ingest(event, context)
        assert "All data has been ingested." in caplog.text

    @mock_aws
    @patch("src.lambda_ingest.put_prev_time")
    @patch("src.lambda_ingest.boto3.client")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.check_database_updated")
    @patch("src.lambda_ingest.connect_to_rds")
    def test_if_updates_in_db_ingested(
        self,
        mock_connect_to_rds,
        mock_check_database_updated,
        mock_get_parameter,
        mock_boto_client,
        mock_put_prev_time,
    ):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect_to_rds.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_check_database_updated.return_value = ["transaction"]
        mock_get_parameter.return_value = "2021-07-27T16:02:08.070557"
        mock_cur.fetchall.return_value = [{"id": 1, "data": "sample data"}]
        mock_cur.description = [("col1",), ("col2",)]
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        mock_put_prev_time.return_value = None
        # Debug prints
        print(f"mock_conn: {mock_conn}")
        print(f"mock_cur: {mock_cur}")
        print(f"mock_conn.cursor(): {mock_conn.cursor()}")
        event = {}
        context = {}
        lambda_handler_ingest(event, context)
        assert mock_get_parameter.call_count == 2

    @mock_aws
    @patch("src.lambda_ingest.put_prev_time")
    @patch("src.lambda_ingest.boto3.client")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.check_database_updated")
    @patch("src.lambda_ingest.connect_to_rds")
    def test_that_file_successfully_uploaded_to_s3(
        self,
        mock_connect_to_rds,
        mock_get_parameter,
        mock_check_database_updated,
        mock_boto_client,
        mock_put_prev_time,
    ):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect_to_rds.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_get_parameter.return_value = "2021-07-27T16:02:08.070557"
        mock_check_database_updated.return_value = ["transaction"]
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        mock_cur.fetchall.return_value = [
            (
                1,
                "PURCHASE",
                1,
                1,
                "2022-11-03 14:20:52.186",
                "2022-11-03 14:20:52.186",
            ),
            (
                2,
                "SALE",
                2,
                2,
                "2022-11-22 17:02:10.130",
                "2022-11-22 17:02:10.130",
            ),
        ]
        mock_cur.description = [("col1",), ("col2",)]
        mock_put_prev_time.return_value = None
        event = {}
        context = {}
        lambda_handler_ingest(event, context)
        assert mock_s3_client.put_object.call_count == 1

    @mock_aws
    @patch("src.lambda_ingest.check_database_updated")
    @patch("src.lambda_ingest.connect_to_rds")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.boto3.client")
    def test_client_error(
        self,
        mock_boto_client,
        mock_get_parameter,
        mock_connect_to_rds,
        mock_check_database_updated,
    ):
        mock_check_database_updated.side_effect = ClientError(
            {"Error": {"Code": "DB connection error"}}, "DB connection error"
        )
        event = {}
        context = {}
        with pytest.raises(
            Exception,
            match="Error interacting with AWS services",
        ):
            lambda_handler_ingest(event, context)


class TestConnection:
    @patch("psycopg2.connect")
    def test_connect_to_rds_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        connection = connect_to_rds()

        mock_connect.assert_called_once_with(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )
        assert connection is mock_connect.return_value

    @patch("psycopg2.connect")
    def test_connect_to_rds_connection_fails_operational_error(
        self, mock_connect, caplog
    ):
        mock_connect.side_effect = psycopg2.OperationalError("mock error")
        connection = connect_to_rds()

        mock_connect.assert_called_once_with(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )

        assert connection is None
        assert "OperationalError connecting to RDS: mock error" in caplog.text

    @patch("psycopg2.connect")
    def test_connect_to_rds_connection_fails_exception_error(
        self, mock_connect
    ):
        mock_connect.side_effect = Exception(
            "Error connection to RDS: Connection error"
        )

        connect_to_rds()

        mock_connect.assert_called_once_with(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )
        with pytest.raises(Exception):
            raise None

    @patch("psycopg2.connect")
    def test_search_rds(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Mock the query result
        mock_cursor.fetchall.return_value = [(1, "USD")]

        connection = connect_to_rds()
        assert connection is not None

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM currency WHERE code = %s", ("USD",))
        results = cursor.fetchall()

        assert results == [(1, "USD")]

        cursor.close()
        close_rds(connection)

        mock_connect.assert_called_once_with(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM currency WHERE code = %s", ("USD",)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_connection.close.assert_called_once()


class TestCloseRds:
    @patch("psycopg2.connect")
    def test_close_rds_closes_database_connection(self, mock_connect, caplog):
        mock_connect = connect_to_rds()

        close_rds(mock_connect)

        assert "Connection to RDS closed" in caplog.text


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
    @pytest.mark.skip
    @mock_aws
    @patch("src.lambda_ingest.retrieve_parameter", side_effect=IndexError)
    @patch("src.lambda_ingest.put_prev_time")
    @patch("boto3.client")
    def test_check_db_updated_returns_all_tables_on_first_invokation(
        self, mock_boto_client, mock_retrieve_parameter, mock_put_prev_time
    ):
        mock_ssm_client = Mock()
        mock_boto_client.return_value = mock_ssm_client
        response = check_database_updated()
        mock_retrieve_parameter.return_value = "2003-12-17T00:00:00"
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

        mock_put_prev_time.return_value = None
        assert response == all_tables

    @patch("src.lambda_ingest.connect_to_rds")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.put_current_time")
    @patch("src.lambda_ingest.put_prev_time")
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

    @patch("src.lambda_ingest.connect_to_rds")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.put_current_time")
    @patch("src.lambda_ingest.put_prev_time")
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

    @patch("src.lambda_ingest.connect_to_rds")
    @patch("src.lambda_ingest.retrieve_parameter")
    @patch("src.lambda_ingest.put_current_time")
    @patch("src.lambda_ingest.put_prev_time")
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
