from application.orchestrators.stock_data_fetch_orchestrators import StockDataFetchOrchestrator
from utilites.technical.technical_agent import technical_agent
from utilites.regime.regime_agent import regime_agent
from utilites.risk.risk_agent import risk_agent
from utilites.fundamental.fundamental_agent import fundamental_agent
from utilites.sentiment.get_sentiment import get_sentiment
from agents.StockSignalAggregatorAgent import StockSignalAggregator
from application.helpers.initializers import SystemInitializer


class StockDataEngine:

    def __init__(self):
        self.stock_data_fetch_orchestrator = StockDataFetchOrchestrator()
        initializer = SystemInitializer()
        self.agents = initializer.get_agents()


    def run(self, symbol: str) -> dict:
        """
        Returns stock data for a given symbol.
        """

        data = self.stock_data_fetch_orchestrator.build_symbol_state(symbol)

        technical_data = technical_agent(data["data"])
        regime_data = regime_agent(data["data"])
        risk_data = risk_agent(data["data"])
        fundamental_data = fundamental_agent(symbol)
        sentiment_data = get_sentiment(symbol)

        mcp_data = {
            "technicals": technical_data,
            "regime_stock": regime_data,
            "risk": risk_data,
            "fundamentals": fundamental_data,
            "sentiment": sentiment_data
        }

        stock_signal_aggregator = StockSignalAggregator(stock_agents=[
            self.agents["technical_agent"],
            self.agents["regime_stock_agent"],
            self.agents["risk_agent"],
            self.agents["fundamental_agent"],
            self.agents["sentiment_agent"]
        ])

        regime_signal = self.agents["regime_stock_agent"].run(symbol, mcp_data)
        aggregated_signals = stock_signal_aggregator.run(symbol, mcp_data, regime_signal)

        return aggregated_signals