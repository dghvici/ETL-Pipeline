from datetime import datetime
import time
import psycopg2

timestamp_prev = None
timestamp_now = None

def check_database_updated():
    """Function to check if the database has been updated since the last
    time it was checked. Returns True if the database has been updated, and
    returns False if there have been no updates to the database"""
    global timestamp_now
    global timestamp_prev

    if timestamp_now == None:
        timestamp_prev = datetime.now()
        timestamp_now = datetime.now()
    else:
        timestamp_prev = timestamp_now
        timestamp_now = datetime.now()

    conn = None
    
    try:
        conn = connect_to_rds()
        cur = conn.cursur()

        table_names = [
            "transaction", "design", "sales_order", "address", 
            "counterparty", "payment", "payment_type", "currency", 
            "staff", "department", "purchase_order"
        ]

        new_dates = []

        for table in table_names:
            query = f"""SELECT last_updated FROM {table} 
            WHERE last_updated BETWEEN '{timestamp_prev}' and '{timestamp_now}'"""
            cur.execute(query)
            new_dates.append(cur.fetchall()) #fetches the rows, returning them as a list of tuples

        output_contains_data = False

        for table_results in new_dates:
            if table_results == []:
                output_contains_data = False
            else:
                output_contains_data = True
                break
        
        return True if output_contains_data else False
    # except:
    #     #add logic here
    finally:
        if conn:
            cur.close()
            close_rds(conn)
    
#find the latest date in last_updated
#OR get the current datetime
#store it to a variable in SSM Parameter Store OR a global variable
#check if the latest date is newer than the variable in parameter store
#return true if it is, false if not

#at the end - assign current_date to previous_date

def lambda_handler():
    #if timestamp_prev is None
        #ingest everything

    #ingest everything between timestamp_prev and timestamp_now
    #SELECT * FROM table WHERE last_updated BETWEEN timestamp_prev and timestamp_now
    pass