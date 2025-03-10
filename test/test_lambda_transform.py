from src.lambda_transform import (
    lambda_handler_transform,
    get_currency,
    create_dataframes,
    create_dim_date,
    upload_dataframes_to_s3,
)
import json
import pandas as pd
import boto3
from moto import mock_aws
import os
import pytest
import io


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY._ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT _REGION"] = "eu-west-2"


class TestGetCurrency:
    def test_get_currency_gives_correct_names(self):
        result_1 = get_currency("GBP")
        result_2 = get_currency("EUR")
        result_3 = get_currency("USD")
        assert result_1 == "pound"
        assert result_2 == "euro"
        assert result_3 == "dollar"

    def test_get_currency_gives_other_for_non_listed_currency(self):
        result_1 = get_currency("RTD")
        assert result_1 == "other"


class TestCreateDataframes:
    def test_create_dataframes_of_expected_type_and_length(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert type(result) is dict
        assert len(result) == 6

    def test_create_dataframes_creates_fact_sales_order(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_fact_sales_order"]) == [
            "sales_records_id",
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id",
        ]

    def test_create_dataframes_creates_dim_staff(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_dim_staff"]) == [
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        ]

    def test_create_dataframes_creates_dim_location(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_dim_location"]) == [
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]

    def test_create_dataframes_creates_dim_design(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_dim_design"]) == [
            "design_id",
            "design_name",
            "file_location",
            "file_name",
        ]

    def test_create_dataframes_creates_dim_currency(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_dim_currency"]) == [
            "currency_id",
            "currency_code",
            "currency_name",
        ]

    def test_create_dataframes_creates_counterparty(self):
        df_tables = {}
        with open("test/transform_test_data.json", "r") as file:
            data = json.load(file)
        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        result = create_dataframes(df_tables)
        assert list(result["df_dim_counterparty"]) == [
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        ]


class TestDimDate:
    def test_create_dim_dates_produces_date_dataframe(self):
        result = create_dim_date()
        assert list(result) == [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
        assert result["year"].values[:1] == [1980]
        assert result["month"].values[:1] == [1]
        assert result["day"].values[:1] == [1]
        assert result["day_of_week"].values[:1] == [1]
        assert result["day_name"].values[:1] == ["Tuesday"]
        assert result["month_name"].values[:1] == ["January"]
        assert result["quarter"].values[:1] == [1]


class TestLambdaHandler:
    def test_lambda_handler_gets_object_from_s3_bucket(
            self, aws_credentials, mocker):
        with mock_aws():
            mock_upload = mocker.patch(
                "src.lambda_transform.upload_dataframes_to_s3")
            bucket_name = "test_bucket"
            s3_client = boto3.client("s3")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            s3_client.create_bucket(
                Bucket="etl-lullymore-west-transformed",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            dummy_data = {
                "New_data": [
                    {
                        "transaction": {
                            "column_names": [
                                "transaction_id",
                                "transaction_type",
                                "sales_order_id",
                                "purchase_order_id",
                                "created_at",
                                "last_updated",
                            ],
                            "rows": [
                                [
                                    1,
                                    "PURCHASE",
                                    None,
                                    2,
                                    "2022-11-03 14:20:52.186000",
                                    "2022-11-03 14:20:52.186000",
                                ]
                            ],
                        }
                    }
                ]
            }
            s3_client.put_object(
                Bucket=bucket_name,
                Key="test_data",
                Body=json.dumps(dummy_data)
            )
            dummy_event = {
                "Records": [
                    {
                        "s3": {
                            "bucket": {"name": bucket_name},
                            "object": {"key": "test_data"},
                        }
                    }
                ]
            }
            lambda_handler_transform(dummy_event, [])
            mock_upload.assert_called_once()


class TestUploadToS3:
    def test_returns_successful_response_message(self, aws_credentials):
        with mock_aws():
            bucket_name = "test_bucket"
            s3_client = boto3.client("s3")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            test_df = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_dict = {"test_table": test_df}
            result = upload_dataframes_to_s3(test_df_dict, bucket_name)
            assert result == "All dataframes uploaded successfully"

    def test_uploads_correct_object_key_to_s3(self, aws_credentials):
        with mock_aws():
            bucket_name = "test_bucket"
            s3_client = boto3.client("s3")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},)
            test_df = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_dict = {"test_table": test_df}
            upload_dataframes_to_s3(
                test_df_dict, bucket_name)
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            obj_keys = [obj["Key"] for obj in objects["Contents"]]
            assert "test_table" in obj_keys[0]

    def test_uploads_multiple_files_to_s3(self, aws_credentials):
        with mock_aws():
            bucket_name = "test_bucket"
            s3_client = boto3.client("s3")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            test_df = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_2 = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_dict = {
                "test_table": test_df, "test_table_2": test_df_2}
            upload_dataframes_to_s3(test_df_dict, bucket_name)
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            obj_keys = [obj["Key"] for obj in objects["Contents"]]
            assert "test_table" in obj_keys[0]
            assert len(obj_keys) == 2
            assert "test_table_2" in obj_keys[1]

    def test_reads_object_as_parquet_successfully(self, aws_credentials):
        with mock_aws():
            bucket_name = "test_bucket"
            s3_client = boto3.client("s3")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            test_df = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_2 = pd.DataFrame(
                {"col1": ["A", "B", "C"], "col2": ["E", "F", "G"]})
            test_df_dict = {"test_table": test_df, "test_table_2": test_df_2}
            upload_dataframes_to_s3(test_df_dict, bucket_name)
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            obj_keys = [obj["Key"] for obj in objects["Contents"]]
            for key in obj_keys:
                obj = s3_client.get_object(Bucket=bucket_name, Key=key)
                buffer = io.BytesIO(obj["Body"].read())
                check_df = pd.read_parquet(buffer, engine="fastparquet")
            assert check_df.equals(test_df)
            assert check_df.equals(test_df_2)
