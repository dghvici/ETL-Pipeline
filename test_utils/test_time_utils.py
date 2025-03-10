import boto3
import os
import pytz #time-aware datetime object
import pytest
from moto import mock_aws
from datetime import datetime
from util_func.python.ingest_utils import (
    put_current_time,
    put_prev_time,
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
    def test_stores_date_parameter_in_parameter_store(
        self, ssm_client):
        tz = pytz.timezone('Europe/London')
        timestamp_prev = tz.localize(datetime(2001, 12, 1, 0, 0, 0)).isoformat()
        put_prev_time(ssm_client, timestamp_prev)
        response = ssm_client.get_parameter(Name="timestamp_prev")
        assert response["Parameter"]["Value"] == timestamp_prev

    def test_stores_time_and_date_parameter_in_parameter_store(
        self, ssm_client):
        tz = pytz.timezone('Europe/London')
        timestamp_prev = tz.localize(datetime(2001, 12, 1, 1, 1)).isoformat()
        put_prev_time(ssm_client, timestamp_prev)
        response = ssm_client.get_parameter(Name="timestamp_prev")
        assert response["Parameter"]["Value"] == timestamp_prev

    def test_raises_value_error_for_invalid_date_format(
        self, ssm_client):
        invalid_timestamp = "2001-12-01T25:01:00"
        with pytest.raises(ValueError):
            put_prev_time(ssm_client, invalid_timestamp)

class TestPutCurrTime:
    def test_stores_date_parameter_in_parameter_store(
        self, ssm_client):
        tz = pytz.timezone('Europe/London')
        timestamp_now = tz.localize(datetime(2003, 12, 17, 0, 0, 0)).isoformat()
        put_current_time(ssm_client, timestamp_now)
        response = ssm_client.get_parameter(Name="timestamp_now")
        assert response["Parameter"]["Value"] == timestamp_now

    def test_stores_date_and_time_parameter_in_parameter_store(
        self, ssm_client):
        tz = pytz.timezone('Europe/London')
        timestamp_now = tz.localize(datetime(2003, 12, 17, 2, 30, 0)).isoformat()
        put_current_time(ssm_client, timestamp_now)
        response = ssm_client.get_parameter(Name="timestamp_now")
        assert response["Parameter"]["Value"] == timestamp_now

    def test_raises_value_error_for_invalid_time(
        self, ssm_client):
        invalid_timestamp = "2003-12-01T25:01:00"
        with pytest.raises(ValueError):
            put_current_time(ssm_client, invalid_timestamp)