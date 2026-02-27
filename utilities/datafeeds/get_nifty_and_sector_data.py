from utilities.datafeeds.download_index import download_index
from utilities.datafeeds.synthetic_basket import synthetic_basket
from utilities.datafeeds.yfinance_config import yf
import pandas as pd


def get_nifty_and_sector_data(sector):

    nifty_series = download_index("^NSEI")

    sector_price_df = pd.concat({

        # 1. BANKING
        "NIFTY BANK": download_index("^NSEBANK"),

        # 2. TECHNOLOGY
        "NIFTY TECHNOLOGY": download_index("^CNXIT"),

        # 3. PHARMA
        "NIFTY PHARMA": download_index("^CNXPHARMA"),

        # 4. FMCG
        "NIFTY FMCG": synthetic_basket([
            "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"
        ]),

        # 5. AUTO
        "NIFTY AUTO": synthetic_basket([
            "MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS"
        ]),

        # 6. METALS
        "NIFTY METAL": synthetic_basket([
            "TATASTEEL.NS", "HINDALCO.NS", "JSWSTEEL.NS", "SAIL.NS"
        ]),

        # 7. ENERGY
        "NIFTY ENERGY": synthetic_basket([
            "RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS"
        ]),

        # 8. INFRASTRUCTURE
        "NIFTY INFRA": synthetic_basket([
            "LT.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "SIEMENS.NS"
        ]),

        # 9. REALTY
        "NIFTY REALTY": synthetic_basket([
            "DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PHOENIXLTD.NS"
        ]),

        # 10. FINANCIAL SERVICES (non-bank)
        "NIFTY FINANCIAL SERVICES": synthetic_basket([
            "BAJFINANCE.NS", "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS"
        ]),

        # 11. CONSUMPTION / RETAIL
        "NIFTY CONSUMER DURABLES": synthetic_basket([
            "TITAN.NS", "TRENT.NS", "DMART.NS", "PAGEIND.NS"
        ]),

        # 12. PSU / DEFENSIVE
        "NIFTY PSU BANK": synthetic_basket([
            "SBIN.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS"
        ]),

        # 13. TELECOM / DIGITAL
        "NIFTY TELECOM": synthetic_basket([
            "BHARTIARTL.NS", "IDEA.NS", "TATACOMM.NS"
        ])

    }, axis=1)


    #stock_series = yf.download("RELIANCE.NS", start="2023-01-01")["Close"]
    stock_sector_series = sector_price_df[sector]

    return nifty_series, sector_price_df, stock_sector_series
