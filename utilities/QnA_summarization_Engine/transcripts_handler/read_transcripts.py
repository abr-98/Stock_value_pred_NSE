from backend_handlers.database_utilities.execute_query import execute_query_to_dataframe

def read_transcripts_from_database(company_slug):

    query = f"""
    SELECT *
    FROM transcripts_3
    WHERE filepath = '{company_slug}'
    ORDER BY date DESC
    LIMIT 4
    """

    df = execute_query_to_dataframe(query)
    return df["url"].tolist()
 