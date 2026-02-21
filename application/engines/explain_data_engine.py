from application.helpers.initializers import SystemInitializer
from application.orchestrators.explaination_data_fetch_orchestrator import DataFetchersExplaination


class ExplainDataEngine:

    def __init__(self, agents=None):
        self.agents = agents  # Pre-initialized agents from API startup
        self.data_fetcher = DataFetchersExplaination()

    def run(self, symbol) -> dict:
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "explain_agent" in self.agents:
            explain_agent = self.agents["explain_agent"]
        else:
            initializer = SystemInitializer()
            initializer.initialize_system()
            agents = initializer.get_agents()
            explain_agent = agents["explain_agent"]

        explaination_state = self.data_fetcher.build_explaination_state(symbol)
        report_text = explain_agent.run(explaination_state["data"])

        analysis = report_text.get("analysis", "")
        rationale = report_text.get("rationale", "")
        
        report = {
            "analysis": analysis,
            "rationale": rationale,
            "symbol": symbol,
            "report_type": "explain_analysis"
        }
        
        return report