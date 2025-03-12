import boto3
from datetime import datetime
import logging
import json

from util_func.python.connection import connect_to_rds, close_rds

ssm = boto3.client("ssm", "eu-west-2")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
