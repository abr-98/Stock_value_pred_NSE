from utilites.allocation.get_propositions import get_propositions
from utilites.serialization_helper import convert_to_serializable

class AllocationAgent:
    def run(self, aggregated_stock_views: dict):
        """
        aggregated_stock_views → output of StockAggregationAgent

        Expected shape (unchanged from your notebook logic):
            symbol → {
                score,
                confidence,
                disagreement,
                ...
            }
        """

        result = get_propositions(aggregated_stock_views)
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)
