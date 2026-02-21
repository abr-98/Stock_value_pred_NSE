from agents.StockSignalAggregatorAgent import StockSignalAggregatorAgent
from agents.TechnicalAgent import TechnicalAgent
from agents.RegimeStockAgent import RegimeStockAgent
from agents.SentimentAgent import SentimentAgent 
from agents.FundamentalAgent import FundamentalAgent
from agents.RiskAgent import RiskAgent
from agents.AllocationAgent import AllocationAgent
from agents.ExplainAgent import ExplainAgent
from agents.PortfolioAnalysisAgent import PortfolioAnalysisAgent
from agents.DiversificationAgent import DiversificationAgent
from agents.CorrelationAgent import CorrelationAgent
from agents.FundamentalDocumentsAgent import FundamentalDocumentsAgent
from agents.MemoryAgent import MemoryAgent

from environment import load_api_key
from application.helpers.vectordb import VectorDB

class SystemInitializer:
    """
    Initializes all agents and orchestrators, and returns them in a dictionary for easy access.
    """

    def __init__(self):
        self.stock_aggregator = None
        self.regime_agent = None
        self.allocation_agent = None
        self.portfolio_agent = None
        self.diversification_agent = None
        self.correlation_agent = None
        self.fundamental_documents_agent = None
        # Individual stock agents
        self.technical_agent = None
        self.sentiment_agent = None
        self.fundamental_agent = None
        self.risk_agent = None
        self.memory_agent = None
        self.explain_agent = None
        

    def initialize_system(self):
        load_api_key()
        VectorDB.initialize_vector_db()

        # Initialize individual stock agents
        technical_agent = TechnicalAgent()
        sentiment_agent = SentimentAgent()
        fundamental_agent = FundamentalAgent()
        risk_agent = RiskAgent()
        memory_agent = MemoryAgent()
        explain_agent = ExplainAgent()
        stock_agents = [
            technical_agent,
            sentiment_agent,
            fundamental_agent,
            risk_agent,
        ]

        stock_aggregator = StockSignalAggregatorAgent(stock_agents)

        regime_agent = RegimeStockAgent()

        allocation_agent = AllocationAgent()
        portfolio_agent = PortfolioAnalysisAgent()
        diversification_agent = DiversificationAgent()
        correlation_agent = CorrelationAgent()
        fundamental_documents_agent = FundamentalDocumentsAgent()

        # Store all agents
        self.stock_aggregator = stock_aggregator
        self.regime_agent = regime_agent
        self.allocation_agent = allocation_agent
        self.portfolio_agent = portfolio_agent
        self.diversification_agent = diversification_agent
        self.correlation_agent = correlation_agent
        self.fundamental_documents_agent = fundamental_documents_agent
        # Store individual stock agents
        self.technical_agent = technical_agent
        self.sentiment_agent = sentiment_agent
        self.fundamental_agent = fundamental_agent
        self.risk_agent = risk_agent
        self.memory_agent = memory_agent
        self.explain_agent = explain_agent

    def get_agents(self):
        return {
            "stock_aggregator": self.stock_aggregator,
            "regime_agent": self.regime_agent,
            "allocation_agent": self.allocation_agent,
            "portfolio_agent": self.portfolio_agent,
            "portfolio_analysis_agent": self.portfolio_agent,  # Alias for compatibility
            "diversification_agent": self.diversification_agent,
            "correlation_agent": self.correlation_agent,
            "fundamental_documents_agent": self.fundamental_documents_agent,
            # Individual stock agents used by stock_data_engine
            "technical_agent": self.technical_agent,
            "sentiment_agent": self.sentiment_agent,
            "fundamental_agent": self.fundamental_agent,
            "risk_agent": self.risk_agent,
            "memory_agent": self.memory_agent,
            "explain_agent": self.explain_agent,
            "regime_stock_agent": self.regime_agent,  # Alias
        }

