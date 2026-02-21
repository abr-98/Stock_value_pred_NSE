from utilities.explaination.get_final_explaination import get_final_explanation
from utilities.explaination.build_impact_explaination_rationale import build_impact_explaination_rationale
from utilities.serialization_helper import convert_to_serializable

class ExplainAgent:

    def run(self, portfolio_mcp_data: dict):
        """
        portfolio_mcp_data MUST match your notebook schema:
        """

        analysis = get_final_explanation(portfolio_mcp_data)

        result = {"analysis": analysis,
                "rationale": build_impact_explaination_rationale(analysis["linear_explanation"], analysis["decision_tree_explanation"])}
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)