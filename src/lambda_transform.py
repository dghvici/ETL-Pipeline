import pandas as pd
# import fastparquet
import json
import boto3
from datetime import datetime as dt
import io


def lambda_handler_transform(event, context):
    s3 = boto3.client('s3')
    transform_bucket = "etl-lullymore-west-transformed"

    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']

    # Trigger an S3 event (JSON file uploaded)- this will be the event
    # Get the object from the event and show its content type\
    df_tables = {}

# Load json data from bucket
    # try:

    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    file_content = response['Body'].read().decode('utf-8')

    data = json.loads(file_content)

    for table_name in data['New_data']:
        df_tables[table_name] = \
            pd.DataFrame(data[table_name]["rows"],
                         columns=data[table_name]["column_names"])

    final_dataframes = {}

    if "sales_order" in df_tables:
        df_sales_order = df_tables["sales_order"]

        # Convert date columns
        df_sales_order['created_at'] = pd.to_datetime(
            df_sales_order['created_at'])
        df_sales_order['last_updated'] = pd.to_datetime(
            df_sales_order['last_updated'])
        df_sales_order['agreed_payment_date'] = pd.to_datetime(
            df_sales_order['agreed_payment_date'])
        df_sales_order['agreed_delivery_date'] = pd.to_datetime(
            df_sales_order['agreed_delivery_date'])

        df_fact_sales_order = pd.DataFrame()
        df_fact_sales_order['sales_records_id'] \
            = range(1, len(df_fact_sales_order) + 1)
        df_fact_sales_order['sales_order_id'] \
            = df_sales_order['sales_order_id']
        df_fact_sales_order['created_date'] \
            = df_sales_order['created_at'].dt.date
        df_fact_sales_order['created_time'] \
            = df_sales_order['created_at'].dt.time
        df_fact_sales_order['last_updated_date'] \
            = df_sales_order['last_updated'].dt.date
        df_fact_sales_order['last_updated_time'] \
            = df_sales_order['last_updated'].dt.time
        df_fact_sales_order['sales_staff_id'] \
            = df_sales_order['staff_id']
        df_fact_sales_order['counterparty_id'] \
            = df_sales_order['counterparty_id']
        df_fact_sales_order['units_sold'] \
            = df_sales_order['units_sold']
        df_fact_sales_order['unit_price'] \
            = df_sales_order['unit_price']
        df_fact_sales_order['currency_id'] \
            = df_sales_order['currency_id']
        df_fact_sales_order['design_id'] \
            = df_sales_order['design_id']
        df_fact_sales_order['agreed_payment_date'] \
            = df_sales_order['agreed_payment_date']
        df_fact_sales_order['agreed_delivery_date'] \
            = df_sales_order['agreed_delivery_date']
        df_fact_sales_order['agreed_delivery_location_id'] \
            = df_sales_order['agreed_delivery_location_id']
        final_dataframes["df_fact_sales_order"] \
            = df_fact_sales_order

    if "staff" in df_tables and "department" in df_tables and \
            "sales_order" in df_tables:
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
        df_dim_location['location_id'] \
            = df_sales_order['agreed_delivery_location']
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
        df_dim_currency['currency_name'] = df_dim_currency['currency_name']\
            .where(df_dim_currency['currency_code'] == 'GBP', 'pound')
        df_dim_currency['currency_name'] = df_dim_currency['currency_name']\
            .where(df_dim_currency['currency_code'] == 'EUR', 'euro')
        df_dim_currency['currency_name'] = df_dim_currency['currency_name']\
            .where(df_dim_currency['currency_code'] == 'USD', 'dollar')

        final_dataframes["df_dim_currency"] = df_dim_currency

    if "counterparty" in df_tables and "address" in df_tables:
        df_counterparty = df_tables["counterparty"]
        df_address = df_tables["address"]

        df_dim_counterparty = pd.DataFrame()
        df_dim_counterparty['counterparty_id'] \
            = df_counterparty['counterparty_id']
        df_dim_counterparty['counterparty_legal_name'] \
            = df_counterparty['counterparty_legal_name']
        df_dim_counterparty['counterparty_legal_address_line_1'] \
            = df_address['address_line_1']
        df_dim_counterparty['counterparty_legal_address_line_2'] \
            = df_address['address_line_2']
        df_dim_counterparty['counterparty_legal_district'] \
            = df_address['district']
        df_dim_counterparty['counterparty_legal_city'] \
            = df_address['city']
        df_dim_counterparty['counterparty_legal_postal_code'] \
            = df_address['postal_code']
        df_dim_counterparty['counterparty_legal_country'] \
            = df_address['country']
        df_dim_counterparty['counterparty_legal_phone_number'] \
            = df_address['number']

        final_dataframes["df_dim_counterparty"] = df_dim_counterparty

    upload_dataframes_to_s3(final_dataframes, transform_bucket)

# dummy_event = {'Records': [{'eventVersion': '2.1', 'eventSource': \
# 'aws:s3', 'awsRegion': 'eu-west-2', 'eventTime': '2025-03-07T12:18:15.393Z',\
#  'eventName': 'ObjectCreated:Put', 'userIdentity': \
# {'principalId': 'AWS:AROA5MSUB6C2VXKYEAC4G:Ingest-Lambda'}, \
# 'requestParameters': {'sourceIPAddress': '18.134.5.40'}, 'responseElements':\
#  {'x-amz-request-id': 'AEHDYJ8G0TBGYPF0', 'x-amz-id-2': \
# 'CfelEx/b0befwraMds2+3bplAobwbQv394xeCkIEjMGrxO1+ZbD5KO2A\
# nqL33r6fE1+ZpWvNjiF7reLxUkpelJYaQhA3HB3o'}, 's3': {'s3SchemaVersion': \
# '1.0', 'configurationId': 'transform-trigger-notification', 'bucket': \
# {'name': 'etl-lullymore-west-ingested', 'ownerIdentity': \
# {'principalId': 'A3C9WEC0881B9E'}, 'arn': 'arn:aws:s3:::\
# etl-lullymore-west-ingested'}, 'object': {'key': \
# '2025/3++++++++++++++++/totesys-data-ingested-2025-03-07+\
# 16%3A57%3A20.144585', 'size': 320, 'eTag': \
# '0f067386df0e327887119e95427e7327', 'sequencer': '0067CAE407595EA004'}}}]}

# if __name__ == '__main__':
#     lambda_handler_transform(dummy_event, 'context')


def upload_dataframes_to_s3(dataframes_dict, transform_bucket):
    s3 = boto3.client('s3')

    for table_name, df in dataframes_dict.items():
        buffer = io.BytesIO()
        df.to_parquet(buffer, engine="fastparquet", compression="gzip")
        buffer.seek(0)

        s3.put_object(
            Bucket=transform_bucket,
            Key=f"{dt.now().year}/{dt.now().month}\
                /transformed-{table_name}-{dt.now()
                                           .strftime(
                                               '%Y-%m-%d_%H-%M-%S')}.parquet",
            Body=buffer.getvalue()
        )

    return "All dataframes uploaded successfully"
