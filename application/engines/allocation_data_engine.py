from application.helpers.initializers import SystemInitializer
from agents.AllocationAgent import AllocationAgent
from application.orchestrators.market_data_fetch_orchestrator import DataFetchOrchestratorMarket


class StockDataEngine:

    def __init__(self, agents=None):
        self.market_fetch_orchestrator = DataFetchOrchestratorMarket()
        self.agents = agents  # Pre-initialized agents from API startup


    def run(self, portfolio, value) -> dict:
        """
        Returns stock data for a given symbol.
        """
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "allocation_agent" in self.agents:
            allocation_agent = self.agents["allocation_agent"]
        else:
            initializer = SystemInitializer()
            agents = initializer.get_agents()
            allocation_agent = agents["allocation_agent"]

        data = self.market_fetch_orchestrator.build_market_state(portfolio, value)
        allocation_analysis = allocation_agent.run(data)

        return {
            "allocation_analysis": allocation_analysis
        }
