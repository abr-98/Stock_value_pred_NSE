from sentence_transformers import CrossEncoder

def fetch_query(vectordb, query):
    # Get initial candidates from similarity search
    results = vectordb.similarity_search_with_relevance_scores(
        query,
        k=10,
    )
    
    if not results:
        return []
    
    # Use cross-encoder for re-ranking
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Prepare documents and scores for cross-encoder
    documents = [doc[0] for doc in results]
    queries = [query] * len(documents)
    
    # Re-rank using cross-encoder
    cross_encoder_scores = cross_encoder.predict([[query, doc.page_content] for doc in documents])
    
    # Combine with original scores and sort by cross-encoder score
    scored_docs = [
        (doc, score) 
        for doc, (_, original_score), score in zip(documents, results, cross_encoder_scores)
    ]
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2 best matching documents
    return [doc for doc, _ in scored_docs[:2]]

