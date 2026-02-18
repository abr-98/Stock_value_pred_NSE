from utilites.portfolio.correlation_agent import correlation_agent
from utilites.portfolio.build_portfolio_rationale import build_portfolio_rationale
from utilites.serialization_helper import convert_to_serializable

class PortfolioAnalysisAgent:
    """
    Delegates portfolio diagnostics to correlation_agent
    """

    def run(self, portfolio_mcp_data: dict):
        """
        portfolio_mcp_data MUST match your notebook schema:

        {
            "prices": {...},
            "weights": {...},
            "sector_map": {...},
            "industry_map": {...}
        }
        """

        analysis = correlation_agent(portfolio_mcp_data)

        result = {"correlation_analysis": analysis,
                "rationale": build_portfolio_rationale(analysis)}
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)