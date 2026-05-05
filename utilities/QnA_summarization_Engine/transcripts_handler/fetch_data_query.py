from sentence_transformers import CrossEncoder
import sys

def fetch_query(vectordb, query):
    """
    Fetch and re-rank documents using cross-encoder.
    
    Args:
        vectordb: Vector database with similarity_search_with_relevance_scores method
        query: Query string
        
    Returns:
        List of top 2 documents ranked by cross-encoder score
    """
    try:
        # Get initial candidates from similarity search
        results = vectordb.similarity_search_with_relevance_scores(
            query,
            k=10,
        )
        
        if not results:
            print(f"No results found for query: {query}", file=sys.stderr)
            return []
        
        print(f"Got {len(results)} initial results for query: {query}", file=sys.stderr)
        
        # Use cross-encoder for re-ranking
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        # Prepare documents and scores for cross-encoder
        documents = [doc[0] for doc in results]
        
        if not documents:
            print(f"No documents extracted from results", file=sys.stderr)
            return []
        
        # Re-rank using cross-encoder
        cross_encoder_scores = cross_encoder.predict([[query, doc.page_content] for doc in documents])
        
        if not cross_encoder_scores or len(cross_encoder_scores) == 0:
            print(f"Cross-encoder returned no scores", file=sys.stderr)
            return documents[:2]  # Fallback to first 2 documents
        
        # Combine with original scores and sort by cross-encoder score
        scored_docs = [
            (doc, score) 
            for doc, (_, original_score), score in zip(documents, results, cross_encoder_scores)
        ]
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 2 best matching documents (or fewer if not available)
        top_docs = [doc for doc, _ in scored_docs[:2]]
        print(f"Returning {len(top_docs)} re-ranked documents", file=sys.stderr)
        
        return top_docs
    except Exception as e:
        print(f"Error in fetch_query: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        # Return empty list on error instead of crashing
        return []

