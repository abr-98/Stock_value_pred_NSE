from utilites.diversification.hierarchical_diversification_agent import hierarchical_diversification_agent
from utilites.diversification.cluster_diagonstics import clustering_diagnostics
from utilites.diversification.build_diversification_rationale import build_hierarchical_diversification_rationale
from utilites.serialization_helper import convert_to_serializable


class DiversificationAgent:
    """
    Structural diversification & concentration authority
    """

    def run(self, portfolio_mcp_data: dict):

        analysis = hierarchical_diversification_agent(
            portfolio_mcp_data["prices"],
            portfolio_mcp_data["weights"],
            portfolio_mcp_data["sector_map"],
            portfolio_mcp_data["industry_map"]
        )

        flags = clustering_diagnostics(
            analysis["asset_level"]  # exactly as your notebook expects
        )

        rationale = build_hierarchical_diversification_rationale(analysis, flags) 

        result = {
            "diversification_analysis": analysis,
            "diagnostic_flags": flags,
            "rationale": rationale
        }
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)
