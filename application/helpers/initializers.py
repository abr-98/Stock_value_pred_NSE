from agents.StockSignalAggregatorAgent import StockSignalAggregator
from agents.TechnicalAgent import TechnicalAgent
from agents.RegimeStockAgent import RegimeStockAgent
from agents.SentimentAgent import SentimentAgent 
from agents.FundamentalAgent import FundamentalAgent
from agents.RiskAgent import RiskAgent
from agents.AllocationAgent import AllocationAgent
from utilites.allocation.unified_sector_allocator_agent import UnifiedSectorAllocatorAgent
from agents.PortfolioAnalysisAgent import PortfolioAnalysisAgent
from agents.DiversificationAgent import DiversificationAgent
from environment import load_api_key
from vectordb import VectorDB

class SystemInitializer:
    """
    Initializes all agents and orchestrators, and returns them in a dictionary for easy access.
    """

    def __init__(self):
        self.stock_aggregator = None,
        self.regime_agent = None,
        self.allocation_agent = None,
        self.portfolio_agent = None,
        self.diversification_agent = None
        

    def initialize_system(self):
        load_api_key()
        VectorDB.initialize_vector_db()

        stock_agents = [
            TechnicalAgent(),
            SentimentAgent(),
            FundamentalAgent(),
            RiskAgent(),

        ]

        stock_aggregator = StockSignalAggregator(stock_agents)

        regime_agent = RegimeStockAgent()

        allocation_agent = AllocationAgent(UnifiedSectorAllocatorAgent())
        portfolio_agent = PortfolioAnalysisAgent()
        diversification_agent = DiversificationAgent()

        self.stock_aggregator = stock_aggregator
        self.regime_agent = regime_agent
        self.allocation_agent = allocation_agent
        self.portfolio_agent = portfolio_agent
        self.diversification_agent = diversification_agent

    def get_agents(self):
        return {
            "stock_aggregator": self.stock_aggregator,
            "regime_agent": self.regime_agent,
            "allocation_agent": self.allocation_agent,
            "portfolio_agent": self.portfolio_agent,
            "diversification_agent": self.diversification_agent
        }
