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
        
        report_text = fundamental_documents_agent.run(symbol)
        
        # Wrap the text report in a dictionary structure for the API response
        report = {
            "analysis": report_text,
            "symbol": symbol,
            "report_type": "fundamental_document_analysis"
        }
        
        return report