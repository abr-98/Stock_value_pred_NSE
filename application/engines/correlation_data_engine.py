from application.orchestrators.correlation_data_fetch_orchestrator import DataFetcherCorrelation
from application.helpers.initializers import SystemInitializer


class CorrelationDataEngine:

    def __init__(self, agents=None):
        self.data_fetcher = DataFetcherCorrelation()
        self.agents = agents  # Pre-initialized agents from API startup


    def run(self, symbol) -> dict:
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

        correlation_report, rationale = correlation_agent.run(self.data_fetcher.fetch_correlation_data(symbol))

        return correlation_report, rationale
