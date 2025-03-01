import os
from unittest.mock import patch, MagicMock
import psycopg2
from utils.connection import connect_to_rds, close_rds
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


@patch("psycopg2.connect")
def test_connect_to_rds_success(mock_connect):
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
        mock_connect, caplog):
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
        mock_connect, caplog):
    mock_connect.side_effect = Exception(
        "Error connection to RDS: Connection error")

    connection = connect_to_rds()

    mock_connect.assert_called_once_with(
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASSWORD"),
        database=os.getenv("RDS_NAME"),
        host=os.getenv("RDS_HOST"),
        port=os.getenv("PORT"),
    )
    assert connection is None
    assert "Error connection to RDS: Connection error" in caplog.text


# retrive 1, 'USD' from currency table


@patch("psycopg2.connect")
def test_search_rds(mock_connect):
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

    # Retrieves data from currency table, validates connection through confirmation that 1) data in first column is an integer, 2) second column is of data type of string

@patch("psycopg2.connect")
def test_connection_retreives_Data_From_rds_database(mock_connect):
    db = connect_to_rds()
    cur = db.cursor()
    response = cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    for table in rows:
        assert isinstance(table[0], int)
        assert isinstance(table[1], str)
    close_rds(db)


@patch("psycopg2.connect")
def test_close_rds_closes_database_connection(mock_connect, caplog):
    mock_connect = connect_to_rds()

    close_rds(mock_connect)

    assert "Connection to RDS closed" in caplog.text
