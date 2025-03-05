import pytest 
from unittest.mock import patch, Mock 
from src.lambda_ingest import lambda_handler_ingest, find_secret, connect_to_rds, close_rds, get_last_imported_timestamp, set_last_imported_timestamp
from botocore.exceptions import ClientError

class TestUtilSecret: 
    @patch("src.lambda_ingest.boto3.client")
    def test_get_secret_happy_path(self, mock_boto_client):
        mock_secretmanager = Mock()
        mock_boto_client.return_value = mock_secretmanager
        mock_secretmanager.find_secret_value= {
            "SecretString": {"username": "user", "password": "password"}
        }
        assert find_secret("secret_name") == {"username": "user", "password": "password"}

    