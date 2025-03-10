# import os
import boto3
from datetime import datetime
import logging

from util_func.python.connection import (
    connect_to_rds, close_rds
)

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
    ssm.put_parameter(
        Name="timestamp_now",
        Description="Time database queried",
        Value=timestamp_now,
        Type="String",
        Overwrite=True,
    )


def retrieve_parameter(ssm, parameter_name, **kwargs):
    try:
        if parameter_name:
            response = ssm.get_parameters(Names=[parameter_name])
        return response["Parameters"][0]["Value"]
    except IndexError:
        logger.error("Error: Name does not exist in Parameter Store")
        raise


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
        timestamp_prev = retrieve_parameter(ssm, "timestamp_now")
        print(timestamp_prev, "prev")
        timestamp_now = datetime.now()
        print(timestamp_now, "now")
        put_current_time(ssm, str(timestamp_now))

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

        put_prev_time(ssm, str(timestamp_now))

        return updated_tables

    except IndexError:
        put_prev_time(ssm, "1981-01-01 00:00:00.000")
        put_current_time(ssm, str(datetime.now()))
        return all_table_names

    finally:
        if conn:
            cur.close()
            close_rds(conn)
