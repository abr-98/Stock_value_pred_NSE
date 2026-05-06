from backend_handlers.database_utilities.execute_query import execute_query_to_dataframe

def read_transcripts_from_database(company_slug, limit=4):
    normalized_slug = (company_slug or "").upper().replace(".NS", "").strip()

    # Prefer company-based match (how feeder stores transcript ownership), then
    # allow filepath-pattern fallback for legacy rows.
    query = f"""
    SELECT company, title, url, filepath, date
    FROM transcripts_3
    WHERE UPPER(company) = '{normalized_slug}'
       OR UPPER(filepath) LIKE '%/{normalized_slug}_%'
       OR UPPER(filepath) LIKE '%\\\\{normalized_slug}_%'
    ORDER BY date DESC
    LIMIT {int(limit)}
    """

    df = execute_query_to_dataframe(query)
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
 