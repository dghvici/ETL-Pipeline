from src.lambda_ingest import lambda_handler_ingest


class TestIngest():

    def test_ingests_all_data_with_empty_db(self):
        # mock db 
        # mock connection
        # ingest mock db
        # assert result is null
        pass

    def test_connection_ingests_all_data(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # ingest mock db
        # assert result is everything in mock db
        pass

    def test_if_no_updates_in_db_no_ingestion_needed(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1= ingest mock db
        # result_2= ingest mock db (capture message --> No new data)
        # assert result_1 == result_2
        # assert response(results_2) == No new data
        pass

    def test_if_updates_in_db_ingested(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1= ingest mock db
        # result_2= ingest mock db (capture message --> No new data)
        # assert result_1 == result_2
        # assert response(results_2) == No new data
        pass

    def test_that_file_successfuly_uploaded_to_s3(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1 = ingest mock db
        # list s3 objects
        # assert result_1 json file name in list s3 object
        pass

    def test_that_data_is_immutable_in_s3(self):
        # mock db 
        # insert data in mock db
        # mock connection
        # result_1 = ingest mock db
        # update db
        # first_ingest_list = list s3 objects
        # result_2 = ingest mock bd
        # second_ingest_list = list s3 objects
        # assert first_ingest != second_ingest
        pass