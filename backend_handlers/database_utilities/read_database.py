import psycopg2
import pandas as pd

def read_table_to_dataframe(table_name, condition):
    """
    Read a PostgreSQL table into a pandas DataFrame

    Args:
        table_name: name of the table to read
        condition: WHERE clause condition
    Returns:
        pandas DataFrame with the table data
    """
    
    conn_params = {
    "host": "localhost",
    "dbname": "Stock_database",
    "user": "postgres",
    "password": "1234",
    "port": 5432
    }

    conn = psycopg2.connect(**conn_params)

    query = f"SELECT * FROM {table_name} WHERE {condition}"
    
    df = pd.read_sql(query, conn)

    conn.close()

    return df
