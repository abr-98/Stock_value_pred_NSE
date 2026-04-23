from utilities.QnA_summarization_Engine.transcripts_handler.query_database_initiator import initiate_query_database
from utilities.QnA_summarization_Engine.transcripts_handler.fetch_data_query import fetch_query


class FetchAndAnswerTool:
    def __init__(self, company_slug):
        self.company_slug = company_slug
        self.vectordb = None
    
    def setup(self):
        self.vectordb = initiate_query_database(self.company_slug)
    
    def answer_query(self, query):
        if self.vectordb is None:
            raise ValueError("Vector database not initialized. Please call setup() first.")
        
        results = fetch_query(self.vectordb, query)
        return results