import pandas as pd
from .fetch_nse_index_gainers import fetch_nse_index

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
        
        #import pandas as pd

        data = fetch_nse_index(index_name)

        if not data:
            return pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])

        df = pd.DataFrame(data)

        # ✅ Remove index row (priority = 1)
        df = df[df["priority"] == 0]

        # ✅ Keep only required columns safely
        required_cols = ["symbol", "lastPrice", "pChange"]
        df = df[[col for col in required_cols if col in df.columns]]

        # If missing columns → return empty
        if len(df.columns) < 3:
            return pd.DataFrame(columns=required_cols)

        # ✅ Convert to numeric (important for sorting)
        df["pChange"] = pd.to_numeric(df["pChange"], errors="coerce")
        df["lastPrice"] = pd.to_numeric(df["lastPrice"], errors="coerce")

        # Drop NaNs just in case
        df = df.dropna(subset=["pChange", "lastPrice"])

        # ✅ Get top gainers
        gainers = (
            df.sort_values("pChange", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        gainers["index"] = index_name
        gainers = gainers[["index", "symbol", "pChange"]]

        return gainers
    
    except Exception:
        # Silently return empty DataFrame - NSE data is optional
        return pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])
