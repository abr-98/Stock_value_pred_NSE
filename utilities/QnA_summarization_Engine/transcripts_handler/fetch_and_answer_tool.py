from utilities.QnA_summarization_Engine.transcripts_handler.query_database_initiator import initiate_query_database
from utilities.QnA_summarization_Engine.transcripts_handler.fetch_data_query import fetch_query
from apis.logging_config import setup_logging, log_service_io


logger = setup_logging("service-utility-qna-fetch-answer")


def _normalize_company_slug(company_slug):
    return (company_slug or "").upper().replace(".NS", "").strip()


class FetchAndAnswerTool:
    _tool_cache = {}
    _vector_cache = {}
    _initialized_companies = set()

    @classmethod
    def get_tool(cls, company_slug):
        normalized_slug = _normalize_company_slug(company_slug)
        tool = cls._tool_cache.get(normalized_slug)
        if tool is None:
            tool = cls(normalized_slug)
            cls._tool_cache[normalized_slug] = tool
        return tool

    def __init__(self, company_slug):
        self.company_slug = _normalize_company_slug(company_slug)
        self.vectordb = None
    
    def setup(self, force_refresh=False):
        log_service_io(
            logger,
            "utility.qna.fetch_and_answer.setup.request",
            inputs={"company_slug": self.company_slug, "force_refresh": force_refresh},
        )

        if (
            not force_refresh
            and self.company_slug in self._initialized_companies
            and self.company_slug in self._vector_cache
        ):
            self.vectordb = self._vector_cache[self.company_slug]
            log_service_io(
                logger,
                "utility.qna.fetch_and_answer.setup.cache_hit",
                outputs={"company_slug": self.company_slug},
            )
            return

        self.vectordb = initiate_query_database(self.company_slug, force_refresh=force_refresh)
        self._vector_cache[self.company_slug] = self.vectordb
        self._initialized_companies.add(self.company_slug)
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