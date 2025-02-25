import psycopg2
from utils.connection import connect_to_rds, close_rds

#Retrieves data from currency table, validates through confirmation that 1) data in first column is an integer, 2) second column is of data type of string
def test_connection_retreives_Data_From_rds_database():

    db = connect_to_rds()
    
    cur = db.cursor()
    reponse = cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    for table in rows:
        assert isinstance(table[0], int) 
        assert isinstance(table[1], str)
    close_rds(db)