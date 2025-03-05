import pytest, os 
import datetime
from unittest.mock import patch, Mock 
from util_func.python.timestamps import get_last_imported_timestamp, set_last_imported_timestamp

class TestUtilTimeStamps:
    def test_last_imported_timestamp_response_is_None(self):
        assert get_last_imported_timestamp() == None

    @patch("util_func.python.timestamps.ssm.put_parameter")
    def test_last_imported_timestamp_returns_mock_data(self, mock_put_parameter):
        set_last_imported_timestamp("2001-12-10")
        mock_put_parameter.assert_called_once_with(
            Name="LastImportedTimeStamp",
            Value="2001-12-10",
            Type="String",
            Overwrite=True
        )
    
    @patch("util_func.python.timestamps.ssm.get_parameter")
    def test_get_last_imported_timestamp(self, mock_get_parameter):
        mock_get_parameter.return_value = {
            "Parameter": {"Value": "2002-12-18"}
        }
        assert get_last_imported_timestamp() == "2002-12-18"


class TestUtilTimestampError:
    @patch("util_func.python.timestamps.ssm.get_parameter")
    def test_get_last_imported_timestamp_error(self, mock_get_parameter):
        mock_get_parameter.side_effect = Exception("Error")
        with pytest.raises(Exception):
            get_last_imported_timestamp()

    @patch("util_func.python.timestamps.ssm.put_parameter")
    def test_set_last_imported_timestamp_error(self, mock_put_parameter):
        mock_put_parameter.side_effect = Exception("Error")
        with pytest.raises(Exception):
            set_last_imported_timestamp("2003-12-01")

           
    