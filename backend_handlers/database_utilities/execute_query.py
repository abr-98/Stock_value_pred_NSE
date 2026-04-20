import psycopg2
import pandas as pd

def execute_query_to_dataframe(query):
    """
    Read a PostgreSQL table into a pandas DataFrame

    Args:
        query: SQL query string
    Returns:
    """
    
    conn_params = {
    "host": "localhost",
    "dbname": "Stock_database",
    "user": "postgres",
    "password": "1234",
    "port": 5432
    }

    conn = psycopg2.connect(**conn_params)
    
    df = pd.read_sql(query, conn)

    conn.close()

    return df
