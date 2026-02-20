from application.orchestrators.correlation_data_fetch_orchestrator import DataFetcherCorrelation
from application.helpers.initializers import SystemInitializer


class CorrelationDataEngine:

    def __init__(self, agents=None):
        self.data_fetcher = DataFetcherCorrelation()
        self.agents = agents  # Pre-initialized agents from API startup


    def run(self, symbol) -> tuple:
        """
        Returns stock data for a given symbol.
        """
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "correlation_agent" in self.agents:
            correlation_agent = self.agents["correlation_agent"]
        else:
            system_initializer = SystemInitializer()
            system_initializer.initialize_system()
            correlation_agent = system_initializer.get_agents()["correlation_agent"]

        result = correlation_agent.run(self.data_fetcher.fetch_correlation_data(symbol))
        
        # Extract analysis and rationale from the result dictionary
        correlation_report = result.get("analysis", {})
        rationale = result.get("rationale", "")

        return correlation_report, rationale
