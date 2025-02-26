import os
import pytest
from unittest.mock import patch, MagicMock
import psycopg2
from utils.connection import connect_to_rds, close_rds
from dotenv import load_dotenv

load_dotenv()


# Retrieves data from currency table, validates connection through confirmation that 1) data in first column is an integer, 2) second column is of data type of string
def test_connection_retreives_Data_From_rds_database():
    db = connect_to_rds()

    cur = db.cursor()
    reponse = cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    for table in rows:
        assert isinstance(table[0], int)
        assert isinstance(table[1], str)
    close_rds(db)


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


# @patch("psycopg2.connect")
# def test_connect_to_rds_connection_fails_operational_error(mock_connect):
#     mock_connect.side_effect = psycopg2.OperationalError("OperationalError connecting to RDS: Connection failed")

#     with pytest.raises(Exception, match="OperationalError connecting to RDS: Connection failed"):
#         connect_to_rds(raise_exception=True)

#     mock_connect.assert_called_once_with(
#         user=os.getenv("RDS_USER"),
#         password=os.getenv("RDS_PASSWORD"),
#         database=os.getenv("RDS_NAME"),
#         host=os.getenv("RDS_HOST"),
#         port=os.getenv("PORT"),
#     )

# @patch("psycopg2.connect")
# def test_connect_to_rds_connection_fails_exception_error(mock_connect):
#     mock_connect.side_effect = Exception("Error connection to RDS: Connection error")

#     connection = connect_to_rds() 

#     mock_connect.assert_called_once_with(
#         user=os.getenv("RDS_USER"),
#         password=os.getenv("RDS_PASSWORD"),
#         database=os.getenv("RDS_NAME"),
#         host=os.getenv("RDS_HOST"),
#         port=os.getenv("PORT"),
#    )
#     assert connection is None 
#     assert "Error connection to RDS: Connection error"