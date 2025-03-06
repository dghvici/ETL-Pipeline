import os
from unittest.mock import patch, MagicMock, Mock 
import psycopg2
from util_func.python.connection import connect_to_rds, close_rds, get_secret
from dotenv import load_dotenv

load_dotenv()

######################################################################
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
    def test_connect_to_rds_connection_fails_exception_error(self, mock_connect, caplog):
        mock_connect.side_effect = Exception(
            "Error connection to RDS: Connection error"
        )

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


    # def test_connection_retreives_Data_From_rds_database():

    #     db = connect_to_rds()
    #     cur = db.cursor()
    #     cur.execute("SELECT * FROM currency")
    #     rows = cur.fetchall()
    #     for table in rows:
    #         assert isinstance(table[0], int)
    #         assert isinstance(table[1], str)
    #     close_rds(db)




######################################################################

class TestCloseRds:
    @patch("psycopg2.connect")
    def test_close_rds_closes_database_connection(self, mock_connect, caplog):
        mock_connect = connect_to_rds()

        close_rds(mock_connect)

        assert "Connection to RDS closed" in caplog.text 

######################################################################
class TestGetSecret:
    @patch("src.lambda_ingest.boto3.client")
    def test_get_secret_happy_path(self, mock_boto_client):
        mock_secretmanager = Mock()
        mock_boto_client.return_value = mock_secretmanager
        mock_secretmanager.get_secret_value= {
            "SecretString": {"username": "user", "password": "password"}
        }
        assert get_secret("secret_name") == {"username": "user", "password": "password"}

    

