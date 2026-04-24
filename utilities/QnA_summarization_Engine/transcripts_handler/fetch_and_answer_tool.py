from utilities.QnA_summarization_Engine.transcripts_handler.query_database_initiator import initiate_query_database
from utilities.QnA_summarization_Engine.transcripts_handler.fetch_data_query import fetch_query
from apis.logging_config import setup_logging, log_service_io


logger = setup_logging("service-utility-qna-fetch-answer")


class FetchAndAnswerTool:
    def __init__(self, company_slug):
        self.company_slug = company_slug
        self.vectordb = None
    
    def setup(self):
        log_service_io(
            logger,
            "utility.qna.fetch_and_answer.setup.request",
            inputs={"company_slug": self.company_slug},
        )
        self.vectordb = initiate_query_database(self.company_slug)
        log_service_io(
            logger,
            "utility.qna.fetch_and_answer.setup.response",
            outputs={"vectordb_initialized": self.vectordb is not None},
        )
    
    def answer_query(self, query):
        if self.vectordb is None:
            raise ValueError("Vector database not initialized. Please call setup() first.")
        log_service_io(
            logger,
            "utility.qna.fetch_and_answer.query.request",
            inputs={"company_slug": self.company_slug, "query": query},
        )
        results = fetch_query(self.vectordb, query)
        log_service_io(
            logger,
            "utility.qna.fetch_and_answer.query.response",
            outputs={"result_count": len(results) if hasattr(results, "__len__") else 0},
        )
        return results