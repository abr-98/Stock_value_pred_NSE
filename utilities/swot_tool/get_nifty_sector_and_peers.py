import yfinance as yf
from .index_maps import *


def get_nifty_sector_and_peers(ticker):
    info = yf.Ticker(ticker).info
    yf_sector = info.get("sector")

    nifty_sector = yf_to_nifty_map.get(yf_sector)

    if not nifty_sector:
        return None, []

    peers = nifty_sector_peers.get(nifty_sector, [])

    return nifty_sector, peers