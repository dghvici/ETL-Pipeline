# import os
import boto3
from datetime import datetime
import logging
import json

<<<<<<< HEAD

# if os.getenv("ENV") == "development":
from connection import connect_to_rds, close_rds

# else:
# from util_func.python.connection import connect_to_rds, close_rds

=======
from util_func.python.connection import connect_to_rds, close_rds
>>>>>>> a2b6426fc63cbe40742628496d817680565fca58

ssm = boto3.client("ssm", "eu-west-2")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def put_prev_time(ssm, timestamp_prev):
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
    formatted_output = {
        table_name: {"column_names": column_names, "rows": rows}
    }
    json_output = json.dumps(formatted_output, default=str)
    return json_output


def check_database_updated():
    """Function to check if the database has been updated since the last time
    it was checked."""
    """Returns a list of the updated table names if the database has been
    updated, and an empty list if there have been no updates to the
    database."""

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
<<<<<<< HEAD
        timestamp_prev = retrieve_parameter(ssm, "timestamp_now")  # 1981
        print(timestamp_prev, "prev in check database util")
        timestamp_now = datetime.now()  # 2025
        print(timestamp_now, "now in check database util")
        put_current_time(ssm, str(timestamp_now))  # 2025
=======
        timestamp_prev = retrieve_parameter(ssm, "timestamp_now")
        timestamp_now = datetime.now()
        put_current_time(ssm, str(timestamp_now))
>>>>>>> a2b6426fc63cbe40742628496d817680565fca58

        conn = connect_to_rds()
        cur = conn.cursor()

        updated_tables = []

        for table in all_table_names:
            query = f"""SELECT last_updated FROM {table}
            WHERE last_updated BETWEEN '{timestamp_prev}'
            and '{timestamp_now}';"""
            cur.execute(query)
            new_dates = (
                cur.fetchall()
            )  # fetches the rows, returning them as a list of tuples
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
