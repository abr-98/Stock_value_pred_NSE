from application.helpers.data_fetcher_report import DataFetchersReport
from utilites.fundamental_document.build_vector_store import build_vector_store

class FundamentalReportFetchOrchestrator:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_market_state(self, symbol) -> dict:

        data_fetcher = DataFetchersReport()
        path = data_fetcher.fetch_annual_report(symbol)

        vector_db = build_vector_store(path)

        return {
            "vector_db": vector_db,
            "report_path": path
        }
