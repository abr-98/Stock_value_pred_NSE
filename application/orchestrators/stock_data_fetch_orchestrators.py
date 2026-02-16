from application.helpers.data_fetchers_stock import DataFetcherStock

class StockDataFetchOrchestrator:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_symbol_state(self, symbol: str) -> dict:

        return {
            "data": DataFetcherStock.get_stock_price(symbol),
            "data_week": DataFetcherStock.get_stock_price_week(symbol)
        }
