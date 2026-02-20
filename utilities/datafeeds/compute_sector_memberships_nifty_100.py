
from utilites.datafeeds import fetch_nse_index


def compute_sector_memberships_nifty_100(nifty100_symbols):
    nifty100_data = fetch_nse_index("NIFTY%20100")
    
    # Handle case where fetch fails
    if nifty100_data is None:
        return {}

    nifty100_symbols = {
        row["symbol"]
        for row in nifty100_data
    }
    SECTOR_INDICES = {
    "IT": "NIFTY%20IT",
    "BANKING": "NIFTY%20BANK",
    "AUTO": "NIFTY%20AUTO",
    "PHARMA": "NIFTY%20PHARMA",
    "FMCG": "NIFTY%20FMCG",
    "METALS": "NIFTY%20METAL",
    "ENERGY": "NIFTY%20ENERGY",
    "REALTY": "NIFTY%20REALTY"
    }

    sector_map = {}

    for sector, index_code in SECTOR_INDICES.items():

        try:
            sector_data = fetch_nse_index(index_code)
            
            # Handle case where fetch returns None
            if sector_data is None:
                sector_map[sector] = []
                continue

            sector_symbols = {
                row["symbol"]
                for row in sector_data
            }

            members = sorted(nifty100_symbols & sector_symbols)
            sector_map[sector] = members

        except Exception as e:
            sector_map[sector] = []

    return sector_map
