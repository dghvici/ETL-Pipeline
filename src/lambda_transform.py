import pandas as pd
import json
import boto3
from datetime import datetime as dt
import io
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm", "eu-west-2")


def put_last_sales_record_id(ssm, sales_record_id):
    """Stores the last sales record ID in AWS SSM Parameter Store.

    This function uploads sales_record_id to AWS SSM Parameter Store as a
    parameter with the name last_sales_record_id.

    Args:
        ssm:
            A boto3 client used to interact with the AWS Parameter Store.
        sales_record_id:
            The sales record ID to be stored in the Parameter Store.

    Returns:
        None: This function does not return any value.
              It stores the sales record ID in the Parameter Store.

    Raises:
        botocore.exceptions.ClientError:
            If there is an error during the interaction with SSM,
            a ClientError will be raised.
    """
    ssm.put_parameter(
        Name="last_sales_record_id",
        Description="last sales record id uploaded to transformed bucket",
        Value=sales_record_id,
        Type="String",
        Overwrite=True,
    )


def retrieve_sales_record_id(ssm, sales_record_id, **kwargs):
    """This function fetches a parameter value from AWS SSM Parameter Store
    based on the provided sales record ID. It attempts to retrieve the value
    associated with the parameter name. If the parameter does not exist, it
    logs an error and raises an exception.

    Args:
        ssm:
            A boto3 client used to interact with the AWS Parameter Store.
        sales_record_id:
            The name of the parameter in Parameter
            Store that holds the sales record ID.
        **kwargs:
            Any additional keyword arguments to be passed.

    Returns:
        The value of the sales record ID retrieved from the
        SSM Parameter Store.

    Raises:
        IndexError: If the parameter does not exist in Parameter Store,
        an `IndexError` will be raised, and an error message will be logged.
    """
    try:
        response = ssm.get_parameters(Names=[sales_record_id])
        return response["Parameters"][0]["Value"]
    except IndexError:
        logger.error("Error: Name does not exist in Parameter Store")
        raise


def get_currency(currency):
    """Returns the name of the currency based on its code.

    This function takes a currency code (e.g., "GBP", "EUR", "USD") and
    returns the name of the currency (e.g., "pound", "euro", "dollar").
    If the currency code is not recognized, it returns "other".

    Args:
        currency: The currency code (e.g., "GBP", "EUR", "USD").

    Returns:
        The name of the currency corresponding to the input code.
        If the code is not recognized, returns "other".
    """
    if currency == "GBP":
        return "pound"
    elif currency == "EUR":
        return "euro"
    elif currency == "USD":
        return "dollar"
    else:
        return "other"


def create_dataframes(df_tables):
    """Transforms and creates fact and dimension dataframes based on input
    tables.

    This function takes a dictionary of dataframes (df_tables).
    The function processes the data, performs necessary transformations,
    and generates fact and dimension dataframes for use in a star schema.

    Args:
        df_tables: A dictionary where the keys are table names and the
        values contain the data for each table.

    Returns:
        dict: A dictionary of transformed dataframes:
            - "df_fact_sales_order": The fact table for sales orders.
            - "df_dim_staff": The dimension table for staff.
            - "df_dim_location": The dimension table for locations.
            - "df_dim_design": The dimension table for designs.
            - "df_dim_currency": The dimension table for currencies.
            - "df_dim_counterparty": The dimension table for counterparties.
    """
    final_dataframes = {}

    if "sales_order" in df_tables:
        df_sales_order = df_tables["sales_order"]

        # Convert date columns
        df_sales_order["created_at"] = pd.to_datetime(
            df_sales_order["created_at"], format="ISO8601"
        )
        df_sales_order["last_updated"] = pd.to_datetime(
            df_sales_order["last_updated"], format="ISO8601"
        )
        df_sales_order["agreed_payment_date"] = pd.to_datetime(
            df_sales_order["agreed_payment_date"], format="ISO8601"
        )
        df_sales_order["agreed_delivery_date"] = pd.to_datetime(
            df_sales_order["agreed_delivery_date"], format="ISO8601"
        )

        df_fact_sales_order = pd.DataFrame()
        df_fact_sales_order["sales_order_id"] = df_sales_order[
            "sales_order_id"
        ]
        df_fact_sales_order["created_date"] = df_sales_order[
            "created_at"
        ].dt.date
        df_fact_sales_order["created_time"] = df_sales_order[
            "created_at"
        ].dt.time
        df_fact_sales_order["last_updated_date"] = df_sales_order[
            "last_updated"
        ].dt.date
        df_fact_sales_order["last_updated_time"] = df_sales_order[
            "last_updated"
        ].dt.time
        df_fact_sales_order["sales_staff_id"] = df_sales_order["staff_id"]
        df_fact_sales_order["counterparty_id"] = df_sales_order[
            "counterparty_id"
        ]
        df_fact_sales_order["units_sold"] = df_sales_order["units_sold"]
        df_fact_sales_order["unit_price"] = df_sales_order["unit_price"]
        df_fact_sales_order["currency_id"] = df_sales_order["currency_id"]
        df_fact_sales_order["design_id"] = df_sales_order["design_id"]
        df_fact_sales_order["agreed_payment_date"] = df_sales_order[
            "agreed_payment_date"
        ]
        df_fact_sales_order["agreed_delivery_date"] = df_sales_order[
            "agreed_delivery_date"
        ]
        df_fact_sales_order["agreed_delivery_location_id"] = df_sales_order[
            "agreed_delivery_location_id"
        ]

        # TO IMPLEMENT:
        # sales_record_id needs to be stored externally via parameter store
        # so the number can continue on each lambda invocation.
        # retrieve at the beginning - in a try block(everything)
        # 1st time: goes into except block and puts to 1
        # be used in range
        # max sent back as variable
        df_fact_sales_order["sales_records_id"] = range(
            1, len(df_fact_sales_order) + 1
        )
        df_fact_sales_order = df_fact_sales_order[
            [
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
        ]
        final_dataframes["df_fact_sales_order"] = df_fact_sales_order

    if "staff" in df_tables and "department" in df_tables:
        df_staff = df_tables["staff"]
        df_department = df_tables["department"]

        df_dim_staff = pd.DataFrame(
            {
                "staff_id": df_staff["staff_id"],
                "first_name": df_staff["first_name"],
                "last_name": df_staff["last_name"],
                "department_name": df_department["department_name"],
                "location": df_department["location"],
                "email_address": df_staff["email_address"],
            }
        )
        final_dataframes["df_dim_staff"] = df_dim_staff

    if "address" in df_tables:
        df_address = df_tables["address"]

        df_dim_location = pd.DataFrame()
        df_dim_location["location_id"] = df_address["address_id"]
        df_dim_location["address_line_1"] = df_address["address_line_1"]
        df_dim_location["address_line_2"] = df_address["address_line_2"]
        df_dim_location["district"] = df_address["district"]
        df_dim_location["city"] = df_address["city"]
        df_dim_location["postal_code"] = df_address["postal_code"]
        df_dim_location["country"] = df_address["country"]
        df_dim_location["phone"] = df_address["phone"]
        final_dataframes["df_dim_location"] = df_dim_location

    if "design" in df_tables:
        df_design = df_tables["design"]

        df_dim_design = pd.DataFrame(
            {
                "design_id": df_design["design_id"],
                "design_name": df_design["design_name"],
                "file_location": df_design["file_location"],
                "file_name": df_design["file_name"],
            }
        )
        final_dataframes["df_dim_design"] = df_dim_design

    if "currency" in df_tables:
        df_currency = df_tables["currency"]

        df_dim_currency = pd.DataFrame()
        df_dim_currency["currency_id"] = df_currency["currency_id"]
        df_dim_currency["currency_code"] = df_currency["currency_code"]
        df_dim_currency["currency_name"] = df_currency["currency_code"].apply(
            get_currency
        )

        final_dataframes["df_dim_currency"] = df_dim_currency

    if "counterparty" in df_tables and "address" in df_tables:
        df_counterparty = df_tables["counterparty"]
        df_address = df_tables["address"]

        df_dim_counterparty = pd.DataFrame()
        df_dim_counterparty["counterparty_id"] = df_counterparty[
            "counterparty_id"
        ]
        df_dim_counterparty["counterparty_legal_name"] = df_counterparty[
            "counterparty_legal_name"
        ]
        df_dim_counterparty["counterparty_legal_address_line_1"] = df_address[
            "address_line_1"
        ]
        df_dim_counterparty["counterparty_legal_address_line_2"] = df_address[
            "address_line_2"
        ]
        df_dim_counterparty["counterparty_legal_district"] = df_address[
            "district"
        ]
        df_dim_counterparty["counterparty_legal_city"] = df_address["city"]
        df_dim_counterparty["counterparty_legal_postal_code"] = df_address[
            "postal_code"
        ]
        df_dim_counterparty["counterparty_legal_country"] = df_address[
            "country"
        ]
        df_dim_counterparty["counterparty_legal_phone_number"] = df_address[
            "phone"
        ]

        final_dataframes["df_dim_counterparty"] = df_dim_counterparty

    return final_dataframes


def create_dim_date():
    """This function generates a dataframe containing a date range from 1980 to
    2040 with columns representing various date attributes.

    Returns:
        pd.DataFrame: A DataFrame with the following columns:
            - date_id: The date (from 1980-01-01 to 2040-12-31)
            - year: The year of the date
            - month: The month of the date (1-12)
            - day: The day of the month (1-31)
            - day_of_week: The weekday index (0=Monday, 6=Sunday)
            - day_name: The name of the day (e.g., "Monday")
            - month_name: The name of the month (e.g., "January")
            - quarter: The quarter of the year (1-4)
    """
    df_dim_date = pd.DataFrame(
        pd.date_range(start="1980-01-01", end="2040-12-31", freq="D"),
        columns=["date_id"],
    )
    df_dim_date["year"] = df_dim_date["date_id"].dt.year
    df_dim_date["month"] = df_dim_date["date_id"].dt.month
    df_dim_date["day"] = df_dim_date["date_id"].dt.day
    df_dim_date["day_of_week"] = df_dim_date["date_id"].dt.weekday
    df_dim_date["day_name"] = df_dim_date["date_id"].dt.day_name()
    df_dim_date["month_name"] = df_dim_date["date_id"].dt.month_name()
    df_dim_date["quarter"] = df_dim_date["date_id"].dt.quarter
    return df_dim_date


def lambda_handler_transform(event, context):
    """Handles the transformation of data from an ingest S3 bucket, processes
    it into dataframes, applies transformations to create a new star schema,
    and uploads the transformed data to a designated S3 bucket.

    Args:
        event: s3 event message in JSON format, containing a record of the
        objects put into the ingest s3 bucket during the
        lambda_handler_ingest run
        context: supplied by AWS

    Returns:
        None: This function does not return a value.
        The transformed data is uploaded directly to S3.

    Raises:
        Exception:
            If there is an error during the S3 interaction or any
            unexpected issue occurs, an exception is raised.
    """
    try:
        s3 = boto3.client("s3")

        source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
        source_key = event["Records"][0]["s3"]["object"]["key"]

        df_tables = {}

        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response["Body"].read().decode("utf-8")

        data = json.loads(file_content)

        for table_dict in data["New_data"]:
            for table_name, table_data in table_dict.items():
                df_tables[table_name] = pd.DataFrame(
                    table_data["rows"], columns=table_data["column_names"]
                )
        final_dataframes = create_dataframes(df_tables)
        final_dataframes["df_dim_dates"] = create_dim_date()

        transform_bucket = "etl-lullymore-west-transformed"
        upload_dataframes_to_s3(final_dataframes, transform_bucket)
        logger.info(
            "All data has been transformed \
                and uploaded to s3 transform bucket"
        )
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception("An unexpected error occurred") from e


def upload_dataframes_to_s3(dataframes_dict, transform_bucket):
    """This function takes a dictionary of DataFrames generated by the
    lambda_handler_transform function, converts each DataFrame to Parquet
    format and uploads them to the provided S3 bucket. The files are organized
    by year and month in the S3 bucket, with each file named using the table
    name and timestamp.

    Args:
        dataframes_dict:
            A dictionary of dataframes created by lambda_handler_transform.
        transform_bucket:
            The name of the target S3 bucket where the Parquet
            files will be uploaded.

    Returns:
        str: A success message indicating that all DataFrames
             have been uploaded to S3.

    Raises:
        Exception: If there is an error while uploading the data to S3,
                   an exception will be raised.
    """

    s3 = boto3.client("s3")

    year = dt.now().year
    month = dt.now().month
    now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")

    for table_name, df in dataframes_dict.items():
        buffer = io.BytesIO()
        df.to_parquet(buffer, engine="fastparquet", compression="gzip")
        buffer.seek(0)

        s3.put_object(
            Bucket=transform_bucket,
            Key=f"{year}/{month}/transformed-{table_name}-{now}.parquet",
            Body=buffer.getvalue(),
        )

    return "All dataframes uploaded successfully"


if __name__ == "__main__":
    lambda_handler_transform("event", "context")
