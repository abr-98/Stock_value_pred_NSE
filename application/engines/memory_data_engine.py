from application.helpers.initializers import SystemInitializer


class MemoryDataEngine:

    def __init__(self, agents=None):
        self.agents = agents  # Pre-initialized agents from API startup

    def run(self, symbol) -> dict:
        # Use pre-initialized agents if available, otherwise initialize
        if self.agents and "memory_agent" in self.agents:
            memory_agent = self.agents["memory_agent"]
        else:
            initializer = SystemInitializer()
            initializer.initialize_system()
            agents = initializer.get_agents()
            memory_agent = agents["memory_agent"]
        
        report_text = memory_agent.run(symbol)
        
        report = {
            "analysis": report_text,
            "symbol": symbol,
            "report_type": "memory_analysis"
        }
        
        return report