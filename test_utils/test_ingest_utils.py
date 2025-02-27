import boto3
from datetime import datetime
import logging
from utils.ingest_utils import *
from moto import mock_aws
import os
import pytest

@pytest.fixture(scope="function")
def aws_credentials():
    """mocked AWS Credentials for moto"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

class TestPutPrevTime:
    def test_put_prev_time_stores_parameter_in_parameter_store(self, aws_credentials):
        with mock_aws():
            test_value = 'test'
            ssm_client = boto3.client("ssm", "eu-west-2")
            put_prev_time(ssm_client, test_value)
            response = ssm_client.get_parameters(
                Names = ["timestamp_prev"])
            assert response['Parameters'][0]['Value'] == test_value

class TestPutCurrTime:
    def test_put_curr_time_stores_parameter_in_parameter_store(self,aws_credentials):
        with mock_aws():
            test_value = 'test'
            ssm_client = boto3.client("ssm", "eu-west-2")
            put_current_time(ssm_client, test_value)
            response = ssm_client.get_parameters(
                Names = ["timestamp_now"])
            assert response['Parameters'][0]['Value'] == test_value

class TestGetParameter:
    def test_get_param_retrieves_param_and_returns_string(self, aws_credentials):
        with mock_aws():
            ssm_client = boto3.client("ssm", "eu-west-2")
            parameter_name = "test_param"
            ssm_client.put_parameter(
                Name=parameter_name, 
                Value="test_value", 
                Type="String",
                Overwrite=True
            )
            response = get_parameter(ssm_client, parameter_name)
            assert response == "test_value"

    def test_get_param_raises_indexerror_if_name_doesnt_exist(self, aws_credentials):
        with mock_aws():
            ssm_client = boto3.client("ssm", "eu-west-2")
            parameter_name = "test_param"
            with pytest.raises(IndexError):
                get_parameter(ssm_client, parameter_name)


class TestCheckDatabaseUpdated:
    def test_check_db_updated_returns_list_of_updated_tables(self):
        pass

    def test_check_db_updated_returns_all_tables_on_first_invokation(self):
        pass  