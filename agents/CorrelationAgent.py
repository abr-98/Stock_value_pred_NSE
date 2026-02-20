from utilites.correlation.market_structure_agent import market_structure_agent
from utilites.correlation.build_correlation_rationale import build_market_sector_rationale
from utilites.serialization_helper import convert_to_serializable

class CorrelationAgent:
    def run(self, nifty_data: dict):
        nifty_series = nifty_data["nifty_series"]
        sector_price_df = nifty_data["sector_price_df"]
        stock_series = nifty_data["stock_series"]
        stock_sector_series = nifty_data["stock_sector_series"]

        analysis = market_structure_agent(nifty_series, sector_price_df, stock_series, stock_sector_series)
        rationale = build_market_sector_rationale(analysis)
    
        result = {"analysis": analysis, "rationale": rationale}
        
        # Convert all numpy/pandas types to Python native types
        return convert_to_serializable(result)
