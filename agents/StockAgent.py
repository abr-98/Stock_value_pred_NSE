from abc import ABC, abstractmethod
from agents.BaseAgent import BaseAgent
from agents.StockSignal import StockSignal

class StockAgent(BaseAgent):
    """
    Base class for stock-specific agents.
    """

    def __init__(self, name: str, horizon: str):
        super().__init__(name)
        self.horizon = horizon

    @abstractmethod
    def run(self, symbol: str, mcp_data: dict) -> StockSignal:
        pass
