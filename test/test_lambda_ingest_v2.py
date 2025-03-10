import pytest
from unittest.mock import patch, Mock
from src.lambda_ingest import (
    lambda_handler_ingest,
    find_secret,
    connect_to_rds,
    close_rds,
    get_last_imported_timestamp,
    set_last_imported_timestamp,
)
from botocore.exceptions import ClientError


class TestUtilAttributes:
    pass
