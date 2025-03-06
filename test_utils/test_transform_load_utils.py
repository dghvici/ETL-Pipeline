from utils.transform_load_utils import get_table_name

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
        #test will need changing when function updated
        file_key = "test"
        expected = None
        result = get_table_name(file_key)
        assert result == expected

