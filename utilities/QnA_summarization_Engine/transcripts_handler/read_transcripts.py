from backend_handlers.database_utilities.execute_query import execute_query_to_dataframe

def read_transcripts_from_database(company_slug, limit=4):
    normalized_slug = (company_slug or "").upper().replace(".NS", "").strip()
    normalized_with_ns = f"{normalized_slug}.NS"

    # Primary match: company can be stored as TCS or TCS.NS depending on feeder input.
    # Fallback path match supports filenames like TCS_* or TCS.NS_*.
    query = f"""
    SELECT company, title, url, filepath, date
    FROM transcripts_3
    WHERE UPPER(company) IN ('{normalized_slug}', '{normalized_with_ns}')
       OR UPPER(filepath) LIKE '%{normalized_slug}_%'
       OR UPPER(filepath) LIKE '%{normalized_with_ns}_%'
    ORDER BY date DESC
    LIMIT {int(limit)}
    """

    df = execute_query_to_dataframe(query)
    if df is None or df.empty:
        # Secondary fallback: match by URL/title text containing the symbol.
        fallback_query = f"""
        SELECT company, title, url, filepath, date
        FROM transcripts_3
        WHERE UPPER(url) LIKE '%{normalized_slug}%'
           OR UPPER(title) LIKE '%{normalized_slug}%'
        ORDER BY date DESC
        LIMIT {int(limit)}
        """
        df = execute_query_to_dataframe(fallback_query)

    if df is None or df.empty:
        return []

    records = []
    for _, row in df.iterrows():
        records.append(
            {
                "url": row.get("url"),
                "filepath": row.get("filepath"),
                "title": row.get("title"),
                "date": row.get("date"),
            }
        )

    return records
 