import psycopg2
from psycopg2.extras import execute_values

def insert_dataframe(df, table_name):
    """
    Insert pandas DataFrame into PostgreSQL table

    Args:
        df: pandas DataFrame
        table_name: target table name
    """
    
    conn_params = {
    "host": "localhost",
    "dbname": "Stock_database",
    "user": "postgres",
    "password": "1234",
    "port": 5432
    }


    if df.empty:
        print("DataFrame is empty. Nothing to insert.")
        return

    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Columns
    cols = list(df.columns)

    # Convert dataframe to list of tuples
    values = [tuple(x) for x in df.to_numpy()]

    # SQL query
    query = f"""
        INSERT INTO {table_name} ({', '.join(cols)})
        VALUES %s
    """

    try:
        execute_values(cursor, query, values)
        conn.commit()
        print(f"Inserted {len(df)} rows into {table_name}")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()