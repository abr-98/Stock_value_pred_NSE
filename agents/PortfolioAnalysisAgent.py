from utilites.portfolio.correlation_agent import correlation_agent

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

        return correlation_agent(portfolio_mcp_data)