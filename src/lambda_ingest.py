import os
import boto3
import json
import logging
import psycopg2
from datetime import datetime
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")
ssm = boto3.client("ssm", "eu-west-2")

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def connect_to_rds(raise_exception=False):
    """connects to Totesys AWS Rational Database Service (RDS) database.
    Note: locally, credentials are supplied by product owner and stored
    locally in gitignored .env. For production, these credentials are
    stored in GitHub Secrets and passed to AWS Sectrets Manager, which
    are is used in place of the .env.

    Errors are logged and raised if there is an problem connecting
    to the database.

    Returns:
        connection: connection to totesys RDS database
    """
    try:
        connection = psycopg2.connect(
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_NAME"),
            host=os.getenv("RDS_HOST"),
            port=os.getenv("PORT"),
        )
        logger.info("Successfully connected to RDS")
        return connection
    except psycopg2.OperationalError as op_error:
        logger.error(f"OperationalError connecting to RDS: {op_error}")
        if raise_exception:
            raise
        return None
    except Exception as error:
        logger.error(f"Error connection to RDS: {error}")
        if raise_exception:
            raise
        return None


def close_rds(conn):
    """Function to close the connection to the RDS database. Logs an error if
    connection is already closed.

    Args:
        conn (connection): connection instance to the database.
    """
    if conn is not None:
        conn.close()
        logger.info("Connection to RDS closed")
    else:
        logger.error("Connection to RDS is already closed")


def put_prev_time(ssm, timestamp_prev):
    """Function to put previous timestamp into the ssm parameter store, for use
    in the lambda_ingest function. Logs an error if the date is in the wrong
    format.

    Args:
        ssm (client): ssm client for AWS
        timestamp_prev (str): previous timestamp as a string
    """
    try:
        datetime.fromisoformat(timestamp_prev)
        ssm.put_parameter(
            Name="timestamp_prev",
            Description="Time database was last queried",
            Value=timestamp_prev,
            Type="String",
            Overwrite=True,
        )
    except ValueError:
        logger.error("Error: Invalid date format")
        raise


def put_current_time(ssm, timestamp_now):
    """Function to put the current timestamp into the ssm parameter store, for
    use in the lambda_ingest function. Logs an error if the date is in the
    wrong format.

    Args:
        ssm (client): ssm client for AWS
        timestamp_now (str): current timestamp as a string
    """
    try:
        datetime.fromisoformat(timestamp_now)
        ssm.put_parameter(
            Name="timestamp_now",
            Description="Time database queried",
            Value=timestamp_now,
            Type="String",
            Overwrite=True,
        )
    except ValueError:
        logger.error("Error: Invalid date format")
        raise


def retrieve_parameter(ssm, parameter_name, **kwargs):
    """Function to retrieve a parameter from the parameter store. Main use case
    for retrieving timestamp_prev and timestamp_now.

    Logs an error and raises and IndexError
    if the parameter does not exist - this can be ignored on
    the first invokation of the lambda_handler_ingest.

    Args:
        ssm (client): ssm client for AWS
        parameter_name (str): name of the parameter to be
        retrieved from the parameter store

    Returns:
        str: value of the parameter
    """
    try:
        if parameter_name:
            response = ssm.get_parameters(Names=[parameter_name])
        return response["Parameters"][0]["Value"]
    except IndexError:
        logger.error(
            "Parameter does not exist in Parameter Store\
                     - ignore error if first invokation"
        )
        raise


def format_raw_data_into_json(table_name, column_names, rows):
    """Function to format raw ingested data from a single table into a suitable
    json format. Data types that are not json serialisable are converted into a
    string.

    Args:
        table_name (str): name of the table to be formatted
        column_names (list): list of column names
        rows (list): list of tuples containing row data

    Returns:
        json: formatted json data
    """
    formatted_output = {
        table_name: {"column_names": column_names, "rows": rows}
    }
    json_output = json.dumps(formatted_output, default=str)
    return json_output


def check_database_updated():
    """Function to check if the database has been updated since the last time
    it was checked.

    Returns:
        list: On the first invokation, returns a list of all the table.
        If the database has been updated, it returns a list of the
        updated table names. If there have been no database updates, an
        empty list is returned.
    """
    conn = None
    all_table_names = [
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

    try:
        timestamp_prev = retrieve_parameter(ssm, "timestamp_now")
        timestamp_now = datetime.now()
        put_current_time(ssm, str(timestamp_now))

        conn = connect_to_rds()
        cur = conn.cursor()

        updated_tables = []

        for table in all_table_names:
            query = f"""SELECT last_updated FROM {table}
            WHERE last_updated BETWEEN '{timestamp_prev}'
            and '{timestamp_now}';"""
            cur.execute(query)
            new_dates = cur.fetchall()
            if new_dates:
                updated_tables.append(table)

        return updated_tables

    except IndexError:
        put_prev_time(ssm, "1981-01-01 00:00:00.000")
        put_current_time(ssm, str(datetime.now()))
        return all_table_names

    finally:
        if conn:
            cur.close()
            close_rds(conn)


def lambda_handler_ingest(event, context):
    """Lambda function to handle the ingest stage of the ETL pipeline. It
    connects to the totesys database, checks if it has been updated since the
    last invokation, formats the updated data into a json file and puts it in
    the etl-lullymore-west-ingested bucket. All data from the updated tables
    are saved into a single JSON file.

    Args:
        event: required for lambda, however is not used in this function
        context: supplied by AWS and required for lambda,
        however is not used in this function

    Error Handling:
        Error handling included to handle issues interacting with
        AWS and unexpected errors. These are also logged as errors.
    """
    try:
        conn = connect_to_rds()
        cur = conn.cursor()
        updated_data_tables = check_database_updated()
        previous_time = retrieve_parameter(ssm, "timestamp_prev")
        current_time = retrieve_parameter(ssm, "timestamp_now")
        if updated_data_tables == []:
            logger.info("No new data.")
        else:
            formatted_output_list = []
            for table in updated_data_tables:
                query = f"""SELECT * FROM {table}
                        WHERE last_updated BETWEEN '{previous_time}'
                        and '{current_time}';"""
                cur.execute(query)
                row_data = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                formatted_output = {
                    table: {"column_names": column_names, "rows": row_data}
                }
                formatted_output_list.append(formatted_output)
            formatted_output = {"New_data": formatted_output_list}
            json_body = json.dumps(formatted_output, default=str)
            s3_client = boto3.client("s3")
            year = datetime.now().year
            month = datetime.now().month
            key = f"{year}/{month}/totesys-data-ingested-{current_time}"
            bucket = "lullymore-west-ingested-2025"
            s3_client.put_object(Bucket=bucket, Key=key, Body=json_body)
            logger.info("All data has been ingested.")
        put_prev_time(ssm, str(current_time))
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception(e)
    finally:
        close_rds(conn)
