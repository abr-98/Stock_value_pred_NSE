from utilites.allocation.get_propositions import get_propositions
from utilites.serialization_helper import convert_to_serializable

class AllocationAgent:
    def run(self, sector_weights=None):
        """
        Get allocation recommendations.
        
        Args:
            sector_weights: Optional dict of current sector weights for diversification
        """

        result = get_propositions(sector_weights)
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)
