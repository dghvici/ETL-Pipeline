import os
from unittest.mock import patch, MagicMock
import psycopg2
import pytest
from util_func.python.connection import connect_to_rds, close_rds
from dotenv import load_dotenv

load_dotenv()


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
