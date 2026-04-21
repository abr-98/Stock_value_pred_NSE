def fetch_query(vectordb, query):
    results = vectordb.similarity_search(
        query,
        k=4,
    )
    return results

