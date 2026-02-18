from application.helpers.initializers import SystemInitializer


class FundamentalReportEngine:

    def __init__(self, agents=None):
        self.agents = agents  # Pre-initialized agents from API startup

    def run(self, symbol) -> dict:
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "fundamental_documents_agent" in self.agents:
            fundamental_documents_agent = self.agents["fundamental_documents_agent"]
        else:
            initializer = SystemInitializer()
            initializer.initialize_system()
            agents = initializer.get_agents()
            fundamental_documents_agent = agents["fundamental_documents_agent"]
        
        report = fundamental_documents_agent.run(symbol)
        return report