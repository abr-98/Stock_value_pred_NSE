from application.helpers.initializers import SystemInitializer
from agents.AllocationAgent import AllocationAgent
from application.orchestrators.market_data_fetch_orchestrator import DataFetchOrchestratorMarket
from utilities.allocation.unified_sector_allocator_agent import UnifiedSectorAllocatorAgent


class StockDataEngine:

    def __init__(self, agents=None):
        self.market_fetch_orchestrator = DataFetchOrchestratorMarket()
        self.agents = agents  # Pre-initialized agents from API startup


    def run(self, portfolio, value) -> dict:
        """
        Returns allocation recommendations.
        
        Args:
            portfolio: Optional dict of {symbol: quantity} for existing holdings
            value: Optional total portfolio value
        """
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "allocation_agent" in self.agents:
            allocation_agent = self.agents["allocation_agent"]
        else:
            initializer = SystemInitializer()
            agents = initializer.get_agents()
            allocation_agent = agents["allocation_agent"]

        # Convert stock portfolio to sector weights if provided
        sector_weights = None
        if portfolio and isinstance(portfolio, dict) and len(portfolio) > 0:
            sector_weights = UnifiedSectorAllocatorAgent.portfolio_to_sector_weights(portfolio)

        allocation_analysis = allocation_agent.run(sector_weights)

        return {
            "allocation_analysis": allocation_analysis
        }
