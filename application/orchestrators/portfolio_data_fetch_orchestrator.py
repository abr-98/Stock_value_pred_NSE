from application.helpers.data_fetchers_portfolio import DataFetchersPortfolio

class PortfolioDataFetchOrchestrator:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_portfolio_state(self, symbol_details, total_portfolio_value) -> dict:

        return DataFetchersPortfolio.get_portfolio_details(symbol_details, total_portfolio_value)
