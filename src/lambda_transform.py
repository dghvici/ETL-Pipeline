import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import boto3
import re
from datetime import datetime as dt
import io


def lambda_handler_transform(event, context):

    transform_bucket = "etl-lullymore-west-transformed"

    s3 = boto3.client('s3')

    #Trigger an S3 event (JSON file uploaded)- this will be the event
    # Get the object from the event and show its content type\
    list_of_keys = []
    list_of_filepath = []

    bucket = event['Records'][0]['s3']['bucket']['name']

    for record in event['Records']:
          list_of_keys.append(record['s3']['object']['key'])
# Load json data from bucket
    try:
        for key in list_of_keys:
            table_name = re.search(r"ingested-(\w+)", key).group(1)
            response = s3.get_object(Bucket=bucket, Key=key)
            file_content = response['Body'].read().decode('utf-8')
            data = json.loads(file_content)
            if table_name == 'counterparty':
                df_counterparty = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'currency':
                df_currency = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'department':
                df_department = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'design':
                df_design = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'staff':
                df_staff = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'sales_order':
                df_sales_order = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'address':
                df_address = pd.DataFrame((data[table_name]["rows"]), columns=data[table_name]["column_names"])

        buffer = io.BytesIO()

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
        df_fact_sales_order['unit_price'] = df_sales_order['unit price']
        df_fact_sales_order['currency_id'] = df_sales_order['currency_id']
        df_fact_sales_order['design_id'] = df_sales_order['design_id']
        df_fact_sales_order['agreed_payment_date'] = df_sales_order['agreed_payment_date']
        df_fact_sales_order['agreed_delivery_date'] = df_sales_order['agreed_delivery_date']
        df_fact_sales_order['agreed_delivery_location_id'] = df_sales_order['agreed_delivery_location_id']
        df_fact_sales_order.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_fact_sales_order-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')

        df_dim_staff = pd.DataFrame()
        df_dim_staff['staff_id'] = df_sales_order['staff_id']
        df_dim_staff['first_name'] = df_staff['first_name']
        df_dim_staff['last_name'] = df_staff['last_name']
        df_dim_staff['department_name'] = df_department['department_name']
        df_dim_staff['location'] = df_department['location']
        df_dim_staff['email_address'] = df_staff['email_address']
        file_path = df_dim_staff.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_dim_staff-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')
        list_of_filepath.append(file_path)



        df_dim_location = pd.DataFrame()
        df_dim_location['location_id'] = df_sales_order['agreed_delivery_location']
        df_dim_location['address_line_1'] = df_address['address_line_1']
        df_dim_location['address_line_2'] = df_address['address_line_2']
        df_dim_location['district'] = df_address['district']
        df_dim_location['city'] = df_address['city']
        df_dim_location['postal_code'] = df_address['postal_code']
        df_dim_location['country'] = df_address['country']
        df_dim_location['phone'] = df_address['phone']
        file_path = df_dim_location.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_dim_location-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')
        list_of_filepath.append(file_path)

        df_dim_design = pd.DataFrame()
        df_dim_design['design_id'] = df_design['design_id']
        df_dim_design['design_name'] = df_design['design_name']
        df_dim_design['file_location'] = df_design['file_location']
        df_dim_design['file_name'] = df_design['file_name']
        file_path = df_dim_location.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_dim_location-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')
        list_of_filepath.append(file_path)

        df_dim_currency = pd.DataFrame()
        df_dim_currency['currency_id'] = df_currency['currency_id']
        df_dim_currency['currency_code'] = df_currency['currency_code']
        df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'GBP', 'pound')
        df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'EUR', 'euro')
        df_dim_currency['currency_name'] = df_dim_currency['currency_name'].where(df_dim_currency['currency_code'] == 'USD', 'dollar')
        file_path = df_dim_currency.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_dim_currency-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')
        list_of_filepath.append(file_path)

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
        file_path = df_dim_counterparty.to_parquet(path=f'{dt.now().year}/{dt.now().month}/transformed-df_dim_counterparty-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet', engine='pyarrow', compression='gzip')
        list_of_filepath.append(file_path)



        for file in list_of_filepath:
            response = s3.put_object(
            Body = file,
            Bucket = transform_bucket,
            Key=f"{dt.now().year}/{dt.now().month}/transformed-{...}-{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            )





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
