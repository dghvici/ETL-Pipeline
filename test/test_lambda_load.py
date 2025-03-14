from src.lambda_load import get_table_name
import pytest


class TestGetTableName:
    def test_get_table_name_returns_transformed_table_name(self):
        file_key = "2025/3/transformed-sales-2025-03-05 15:00:22.634136"
        expected = "sales"
        result = get_table_name(file_key)
        assert result == expected

    def test_get_table_name_returns_ingested_table_name(self):
        file_key = "2025/3/ingested-sales-2025-03-05 15:00:22.634136"
        expected = "sales"
        result = get_table_name(file_key)
        assert result == expected

    def test_get_table_name_returns_blank(self):
        with pytest.raises(UnboundLocalError):
            file_key = "test"
            get_table_name(file_key)


# tests required for load_lambda
# test that data has been loaded into mock data warehouse (all tables)
# test that the loggers have logged the appropriate information
# test that data has been appended to the data warehouse (not overwritten)

# manual integration tests when deployed to AWS required to check pipeline
# correctly works and datawarehouse updated
