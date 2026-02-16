from application.helpers.initializers import SystemInitializer
from agents.AllocationAgent import AllocationAgent
from application.orchestrators.market_data_fetch_orchestrator import DataFetchOrchestratorMarket


class StockDataEngine:

    def __init__(self):
        self.market_fetch_orchestrator = DataFetchOrchestratorMarket()


    def run(self, portfolio, value) -> dict:
        """
        Returns stock data for a given symbol.
        """
        initializer = SystemInitializer()
        agents = initializer.get_agents()

        data = self.market_fetch_orchestrator.build_market_state(portfolio, value)
        allocation_agent = agents["allocation_agent"]
        allocation_analysis = allocation_agent.run(data)

        return {
            "allocation_analysis": allocation_analysis
        }
