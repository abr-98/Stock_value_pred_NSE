from .top_gainers_in_sector_nse import top_gainers_in_sector
import pandas as pd
import datetime


def get_market_positions():
    """
    Get market positions for top gainers in key sectors.
    Returns a dict with sector as key and list of top gainers as value.
    """
    nifty_indices = [
    "NIFTY%2050",
    "NIFTY%20NEXT%2050",
    "NIFTY%20100",
    "NIFTY%20200",
    "NIFTY%20500",

    "NIFTY%20BANK",
    "NIFTY%20FINANCIAL%20SERVICES",
    "NIFTY%20PRIVATE%20BANK",
    "NIFTY%20PSU%20BANK",

    "NIFTY%20IT",
    "NIFTY%20PHARMA",
    "NIFTY%20FMCG",
    "NIFTY%20AUTO",
    "NIFTY%20METAL",
    "NIFTY%20REALTY",
    "NIFTY%20MEDIA",
    "NIFTY%20ENERGY",
    "NIFTY%20INFRA",
    "NIFTY%20CONSUMER%20DURABLES",
    "NIFTY%20OIL%20%26%20GAS",

    "NIFTY%20MIDCAP%20100",
    "NIFTY%20MIDCAP%20150",
    "NIFTY%20MIDCAP%20SELECT",

    "NIFTY%20SMALLCAP%20100",
    "NIFTY%20SMALLCAP%20250",

    "NIFTY%20TOTAL%20MARKET",
    "NIFTY%20MICROCAP%20250"
]
    market_positions = {}

    for index_code in nifty_indices:
        gainers_df = top_gainers_in_sector(index_code)
        gainers_list = gainers_df.to_dict(orient="records")
        market_positions[index_code] = gainers_list

    df = pd.DataFrame([item for sublist in market_positions.values() for item in sublist])
    
    df["date"] = datetime.datetime.now().date()
    
    
    return df
    