from application.orchestrators.fundamental_report_fetch_orchestrator import FundamentalReportFetchOrchestrator
from agents.FundamentalRAGSystem import FundamentalRAGSystem
from application.helpers.vectordb import VectorDB


class FundamentalReportEngine:

    def __init__(self):
        self.data_fetcher = FundamentalReportFetchOrchestrator()



    def run(self, symbol) -> dict:
        """
        Returns stock data for a given symbol.
        """

        market_state = self.data_fetcher.build_market_state(symbol)

        vector_db = market_state["vector_db"]

        rag_system = FundamentalRAGSystem(vector_db)
        report = rag_system.explain_company(symbol)

        return report
