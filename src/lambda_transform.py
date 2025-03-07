import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import boto3
import re
from datetime import datetime as dt
import io


def lambda_handler_transform(event, context):
    s3 = boto3.client('s3')
    transform_bucket = "etl-lullymore-west-transformed"

    source_bucket = event['Records'][0]['s3']['bucket']['name']

    #Trigger an S3 event (JSON file uploaded)- this will be the event
    # Get the object from the event and show its content type\
    df_tables = {}
    final_dataframes = {}

    list_of_keys = [record['s3']['object']['key'] for record in event['Records']]
# Load json data from bucket
    try:
        for key in list_of_keys:
            table_name = re.search(r"ingested-(\w+)", key).group(1)
            response = s3.get_object(Bucket=source_bucket, Key=key)
            file_content = response['Body'].read().decode('utf-8')
            data = json.loads(file_content)

            df_tables[table_name] = pd.DataFrame(data[table_name]["rows"], columns=data[table_name]["column_names"])

            final_dataframes = {}

        if "sales_order" in df_tables:
            df_sales_order = df_tables["sales_order"]
            
            # Convert date columns
            df_sales_order['created_at'] = pd.to_datetime(df_sales_order['created_at'])
            df_sales_order['last_updated'] = pd.to_datetime(df_sales_order['last_updated'])
            df_sales_order['agreed_payment_date'] = pd.to_datetime(df_sales_order['agreed_payment_date'])
            df_sales_order['agreed_delivery_date'] = pd.to_datetime(df_sales_order['agreed_delivery_date'])



            df_fact_sales_order = pd.DataFrame()
            df_fact_sales_order['sales_records_id'] = range(1, len(df_fact_sales_order) + 1)
            df_fact_sales_order['sales_order_id'] = df_sales_order['sales_order_id']
            df_fact_sales_order['created_date'] = df_sales_order['created_at'].dt.date
            df_fact_sales_order['created_time'] = df_sales_order['created_at'].dt.time
            df_fact_sales_order['last_updated_date'] = df_sales_order['last_updated'].dt.date
            df_fact_sales_order['last_updated_time'] = df_sales_order['last_updated'].dt.time
            df_fact_sales_order['sales_staff_id'] = df_sales_order['staff_id']
            df_fact_sales_order['counterparty_id'] = df_sales_order['counterparty_id']
            df_fact_sales_order['units_sold'] = df_sales_order['units_sold']
            df_fact_sales_order['unit_price'] = df_sales_order['unit_price']
            df_fact_sales_order['currency_id'] = df_sales_order['currency_id']
            df_fact_sales_order['design_id'] = df_sales_order['design_id']
            df_fact_sales_order['agreed_payment_date'] = df_sales_order['agreed_payment_date']
            df_fact_sales_order['agreed_delivery_date'] = df_sales_order['agreed_delivery_date']
            df_fact_sales_order['agreed_delivery_location_id'] = df_sales_order['agreed_delivery_location_id']
            final_dataframes["df_fact_sales_order"] = df_fact_sales_order
        
        if "staff" in df_tables and "department" in df_tables and "sales_order" in df_tables:
            df_staff = df_tables["staff"]
            df_department = df_tables["department"]
            df_sales_order = df_tables["sales_order"]
            
            df_dim_staff = pd.DataFrame({
                "staff_id": df_sales_order['staff_id'],
                "first_name": df_staff['first_name'],
                "last_name": df_staff['last_name'],
                "department_name": df_department['department_name'],
                "location": df_department['location'],
                "email_address": df_staff['email_address'],
            })
            final_dataframes["df_dim_staff"] = df_dim_staff

        if "address" in df_tables and "sales_order" in df_tables:
            df_address = df_tables["address"]
            df_sales_order = df_tables["sales_order"]

            df_dim_location = pd.DataFrame()
            df_dim_location['location_id'] = df_sales_order['agreed_delivery_location']
            df_dim_location['address_line_1'] = df_address['address_line_1']
            df_dim_location['address_line_2'] = df_address['address_line_2']
            df_dim_location['district'] = df_address['district']
            df_dim_location['city'] = df_address['city']
            df_dim_location['postal_code'] = df_address['postal_code']
            df_dim_location['country'] = df_address['country']
            df_dim_location['phone'] = df_address['phone']
            final_dataframes["df_dim_location"] = df_dim_location

        if "design" in df_tables:
            df_design = df_tables["design"]

            df_dim_design = pd.DataFrame({
                "design_id": df_design['design_id'],
                "design_name": df_design['design_name'],
                "file_location": df_design['file_location'],
                "file_name": df_design['file_name'],
        })
        final_dataframes["df_dim_design"] = df_dim_design



        if "currency" in df_tables:
            df_currency = df_tables["currency"]
            
            df_dim_currency = pd.DataFrame()
            df_dim_currency['currency_id'] = df_currency['currency_id']
            df_dim_currency['currency_code'] = df_currency['currency_code']
            df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'GBP', 'pound')
            df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'EUR', 'euro')
            df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'USD', 'dollar')

            final_dataframes["df_dim_currency"] = df_dim_currency

        

        if "counterparty" in df_tables and "address" in df_tables:
            df_counterparty = df_tables["counterparty"]
            df_address = df_tables["address"]

            df_dim_counterparty = pd.DataFrame()
            df_dim_counterparty['counterparty_id'] = df_counterparty['counterparty_id']
            df_dim_counterparty['counterparty_legal_name'] = df_counterparty['counterparty_legal_name']
            df_dim_counterparty['counterparty_legal_address_line_1'] = df_address['address_line_1']
            df_dim_counterparty['counterparty_legal_address_line_2'] = df_address['address_line_2']
            df_dim_counterparty['counterparty_legal_district'] = df_address['district']
            df_dim_counterparty['counterparty_legal_city'] = df_address['city']
            df_dim_counterparty['counterparty_legal_postal_code'] = df_address['postal_code']
            df_dim_counterparty['counterparty_legal_country'] = df_address['country']
            df_dim_counterparty['counterparty_legal_phone_number'] = df_address['number']

            final_dataframes["df_dim_counterparty"] = df_dim_counterparty

        upload_dataframes_to_s3(final_dataframes, transform_bucket)
        
        
        def upload_dataframes_to_s3(dataframes_dict, transform_bucket):
            s3 = boto3.client('s3')


        
            for table_name, df in dataframes_dict.items():
                buffer = io.BytesIO()
                df.to_parquet(buffer, engine="pyarrow", compression="gzip")
                buffer.seek(0)

                s3.put_object(
                    Bucket=transform_bucket,
                    Key=f"{dt.now().year}/{dt.now().month}/transformed-{table_name}-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet",
                    Body=buffer.getvalue()
                )

            return "All dataframes uploaded successfully"



        # for file in list_of_filepath:
        #     response = s3.put_object(
        #     Body = file,
        #     Bucket = transform_bucket,
        #     Key=f"{dt.now().year}/{dt.now().month}/transformed-{...}-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        #     )





# CASE WHEN in pandas:
#     pd_df["difficulty"] = "Unknown"
#     pd_df["difficulty"] = pd_df["difficulty"].case_when([
#     (pd_df.eval("0 < Time < 30"), "Easy"), 
#     (pd_df.eval("30 <= Time <= 60"), "Medium"), 
#     (pd_df.eval("Time > 60"), "Hard")
# ])


#   INSERT INTO client_summary (client, quantity, total) SELECT client, SUM(quantity) AS quantity, SUM(total) AS totalFROM enriched_fact_table GROUP BY client;

# result['serial_key'] = range(1, len(result) + 1)
# df1 = df1[[column names in order you want]]

    

# expected input == {tablename: {"column_names": ["col1", "col2", "col3"], "rows": [(1, 100, "abc'def"), (2, None, 'dada'), (3, 42, 'bar')]}

# Load json data from bucket (json.loads - unsure if needed to transform json data, as ingestion phase ingests as dict of tuples)
# import boto3
# import json

# s3 = boto3.resource('s3')

# content_object = s3.Object('test', 'sample_json.txt')
# file_content = content_object.get()['Body'].read().decode('utf-8')
# json_content = json.loads(file_content)
# print(json_content['Details'])
#transform json data to DF
#Convert DF to pyarrow table
#output as parquet
#Load this to the transformation bucket



# CREATE TABLE fact_sales_order
#                     (
#                     sales_record_id SERIAL PRIMARY KEY,
#                     sales_order_id INT,
#                     created_date DATE,
#                     created_time TIME,
#                     last_updated_date DATE,
#                     last_updated_TIME,
#                     sales_staff_id INT,
#                     counterparty_id INT,
#                     units_sold INT,
#                     unit_price NUMERIC,
#                     currency_id INT,
#                     design_id INT,
#                     agreed_payment_date DATE,
#                     agreed_delivery_date DATE,
#                     agreed_delivery_location_id INT
#                     );
#                     INSERT INTO fact_sales_order
#                     (sales_order_id, created_date, created_time, last_updated_date, last_updated, sales_staff_id, counterparty_id,
#                     units_sold, unit_price, currency_id, design_id, agreed_payment_date, agreed_delivery_date, agreed_delivery_location_id)
                    #   SELECT
                    #     sa.sales_order_id,
                    #     DATE(sa.created_at) AS created_date,
                    #     TIME(sa.created_at) AS created_time,
                    #     DATE(sa.last_updated) AS last_updated_date,
                    #     TIME(sa.last_updated) AS last_updated_time,
                    #     sa.staff_id AS sales_staff_id,
                    #     counterparty_id,
                    #     units_sold
                    # FROM
                    #     df_sales_order AS sa



# placeholder for the purpose of the CICD pipeline
# do not change lambda handler name --> linked to tf lamda handler resource

#Import


    return True
