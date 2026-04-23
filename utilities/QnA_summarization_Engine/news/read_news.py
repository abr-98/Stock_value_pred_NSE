from backend_handlers.database_utilities.execute_query import execute_query_to_dataframe

def read_news_from_database(company_slug):
    
    from datetime import datetime, timedelta

    date_str = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    query = f"""
    SELECT *
    FROM news_2
    WHERE company = '{company_slug}'
    AND MAKE_DATE(year, month, day) >= '{date_str}'
    """

    df = execute_query_to_dataframe(query)
    return df