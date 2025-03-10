


class TestRetreieveParameter:
    @mock_aws
    def test_retreieve_param_retrieves_param_and_returns_string(self):
        ssm_client = boto3.client("ssm", "eu-west-2")
        parameter_name = "test_param"
        ssm_client.put_parameter(
            Name=parameter_name,
            Value="test_value",
            Type="String",
            Overwrite=True,
        )
        response = retrieve_parameter(ssm_client, parameter_name)
        assert response == "test_value"

    @mock_aws
    def test_get_param_raises_indexerror_if_name_doesnt_exist(self):
        ssm_client = boto3.client("ssm", "eu-west-2")
        parameter_name = "test_param"
        with pytest.raises(IndexError):
            retrieve_parameter(ssm_client, parameter_name)


class TestCheckDatabaseUpdated:
    @patch(
        "util_func.python.ingest_utils.retrieve_parameter",
        side_effect=IndexError,
    )
    def test_check_db_updated_returns_all_tables_on_first_invokation(
        self, mock_retrieve_parameter
    ):
        check_database_updated()

    all_tables = [
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

    assert response == all_tables
