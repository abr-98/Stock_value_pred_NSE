import pandas as pd
from utilites.datafeeds.fetch_nse_index import fetch_nse_index

def top_gainers_in_sector(index_name: str, top_n: int = 5):
    """
    Example inputs:
        "NIFTY%20IT"
        "NIFTY%20BANK"
        "NIFTY%20AUTO"
    """

    data = fetch_nse_index(index_name)

    df = pd.DataFrame(data)

    gainers = (
        df.sort_values("pChange", ascending=False)
          [["symbol", "lastPrice", "pChange"]]
          .head(top_n)
          .reset_index(drop=True)
    )

    return gainers
