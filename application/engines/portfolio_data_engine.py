from application.orchestrators.portfolio_data_fetch_orchestrator import PortfolioDataFetchOrchestrator
from application.helpers.initializers import SystemInitializer


class PortfolioDataEngine:

    def __init__(self, agents=None):
        self.portfolio_fetch_orchestrator = PortfolioDataFetchOrchestrator()
        self.agents = agents  # Pre-initialized agents from API startup


    def run(self, portfolio, value) -> dict:
        """
        Returns stock data for a given symbol.
        """
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "portfolio_analysis_agent" in self.agents and "diversification_agent" in self.agents:
            portfolio_analysis_agent = self.agents["portfolio_analysis_agent"]
            diversification_agent = self.agents["diversification_agent"]
        else:
            initializer = SystemInitializer()
            agents = initializer.get_agents()
            portfolio_analysis_agent = agents["portfolio_analysis_agent"]
            diversification_agent = agents["diversification_agent"]

        data = self.portfolio_fetch_orchestrator.build_portfolio_state(portfolio, value)
        portfolio_analysis, portfolio_rationale = portfolio_analysis_agent.run(data)
        diversification_analysis, diversification_rationale = diversification_agent.run(data)

        rationale = f"Portfolio Analysis Rationale: {portfolio_rationale}\n\nDiversification Analysis Rationale: {diversification_rationale}" 

        return {
            "portfolio_analysis": portfolio_analysis,
            "diversification_analysis": diversification_analysis,
            "rationale": rationale
        }
