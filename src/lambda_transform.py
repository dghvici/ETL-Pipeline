import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
import json
import boto3
import re


def lambda_handler_transform(event, context):

    s3 = boto3.client('s3')

    #Trigger an S3 event (JSON file uploaded)- this will be the event
    # Get the object from the event and show its content type\
    list_of_keys = []
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
                df_counterparty = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'currency':
                df_currency = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'department':
                df_department = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'design':
                df_design = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'staff':
                df_staff = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'sales_order':
                df_sales_order = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])
            elif table_name == 'address':
                df_address = pd.Dataframe((data[table_name]["rows"]), columns=data[table_name]["column_names"])

        query_fact_sales_order = '''
                  CREATE TABLE fact_sales_order
                    (
                    sales_record_id SERIAL PRIMARY KEY,
                    sales_order_id INT,
                    created_date DATE,
                    created_time TIME,
                    last_updated_date DATE,
                    last_updated_TIME,
                    sales_staff_id INT,
                    counterparty_id INT,
                    units_sold INT,
                    unit_price NUMERIC,
                    currency_id INT,
                    design_id INT,
                    agreed_payment_date DATE,
                    agreed_delivery_date DATE,
                    agreed_delivery_location_id INT
                    );
                    INSERT INTO fact_sales_order
                    (sales_order_id, created_date, created_time, last_updated_date, last_updated, sales_staff_id, counterparty_id,
                    units_sold, unit_price, currency_id, design_id, agreed_payment_date, agreed_delivery_date, agreed_delivery_location_id)
                    SELECT
                        sa.sales_order_id,
                        DATE(sa.created_at) AS created_date,
                        TIME(sa.created_at) AS created_time,
                        DATE(sa.last_updated) AS last_updated_date,
                        TIME(sa.last_updated) AS last_updated_time,
                        sa.staff_id AS sales_staff_id,
                    FROM
                        sales_order AS sa
                        '''
        
     #   INSERT INTO client_summary (client, quantity, total) SELECT client, SUM(quantity) AS quantity, SUM(total) AS totalFROM enriched_fact_table GROUP BY client;

    

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




# placeholder for the purpose of the CICD pipeline
# do not change lambda handler name --> linked to tf lamda handler resource

#Import


    return True
