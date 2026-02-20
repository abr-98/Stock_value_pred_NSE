import pandas as pd
from utilites.datafeeds.fetch_nse_index import fetch_nse_index

def top_gainers_in_sector(index_name: str, top_n: int = 5):
    """
    Get top gaining stocks in a sector index.
    
    Example inputs:
        "NIFTY%20IT"
        "NIFTY%20BANK"
        "NIFTY%20AUTO"
    
    Returns:
        DataFrame with columns: symbol, lastPrice, pChange
        Returns empty DataFrame if fetch fails
    """
    try:
        data = fetch_nse_index(index_name)
        
        # Check if data was successfully fetched
        if data is None or len(data) == 0:
            return pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])

        df = pd.DataFrame(data)
        
        # Ensure required columns exist
        if not all(col in df.columns for col in ["symbol", "lastPrice", "pChange"]):
            return pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])

        gainers = (
            df.sort_values("pChange", ascending=False)
              [["symbol", "lastPrice", "pChange"]]
              .head(top_n)
              .reset_index(drop=True)
        )

        return gainers
    
    except Exception:
        # Silently return empty DataFrame - NSE data is optional
        return pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])
