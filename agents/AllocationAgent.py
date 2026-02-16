from utilites.allocation.get_propositions import get_propositions

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

        return get_propositions(aggregated_stock_views)
