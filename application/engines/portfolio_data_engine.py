from application.orchestrators.portfolio_data_fetch_orchestrator import PortfolioDataFetchOrchestrator
from application.helpers.initializers import SystemInitializer


class StockDataEngine:

    def __init__(self):
        self.portfolio_fetch_orchestrator = PortfolioDataFetchOrchestrator()


    def run(self, portfolio, value) -> dict:
        """
        Returns stock data for a given symbol.
        """
        initializer = SystemInitializer()
        agents = initializer.get_agents()

        data = self.portfolio_fetch_orchestrator.build_portfolio_state(portfolio, value)
        portfolio_analysis_agent = agents["portfolio_analysis_agent"]
        diversification_agent = agents["diversification_agent"]
        portfolio_analysis = portfolio_analysis_agent.run(data)
        diversification_analysis = diversification_agent.run(data)

        return {
            "portfolio_analysis": portfolio_analysis,
            "diversification_analysis": diversification_analysis
        }
