import psycopg2
from psycopg2.extras import execute_values

def insert_dataframe(df, table_name, unique_columns=None):
    """
    Insert pandas DataFrame into PostgreSQL table

    Args:
        df: pandas DataFrame
        table_name: target table name
        unique_columns: list of columns that should be unique (optional)
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
    
    if unique_columns is not None:
        
        # SQL query
        query = f"""
            INSERT INTO {table_name} ({', '.join(cols)})
            VALUES %s
            ON CONFLICT ({', '.join(unique_columns)}) DO NOTHING
        """
    else:
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