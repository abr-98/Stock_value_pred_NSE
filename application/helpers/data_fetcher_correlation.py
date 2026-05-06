from utilities.datafeeds.get_nifty_and_sector_data import get_nifty_and_sector_data
from utilities.datafeeds.get_stock_series import get_stock_series
from utilities.datafeeds.get_sector import get_sector_yf


SECTOR_TO_NIFTY_KEY = {
    # yfinance style sector names
    "TECHNOLOGY": "NIFTY TECHNOLOGY",
    "FINANCIAL SERVICES": "NIFTY FINANCIAL SERVICES",
    "HEALTHCARE": "NIFTY PHARMA",
    "CONSUMER DEFENSIVE": "NIFTY FMCG",
    "CONSUMER CYCLICAL": "NIFTY CONSUMER DURABLES",
    "COMMUNICATION SERVICES": "NIFTY TELECOM",
    "REAL ESTATE": "NIFTY REALTY",
    "INDUSTRIALS": "NIFTY INFRA",
    "BASIC MATERIALS": "NIFTY METAL",
    "ENERGY": "NIFTY ENERGY",
    "UTILITIES": "NIFTY ENERGY",

    # direct NIFTY-like aliases
    "BANK": "NIFTY BANK",
    "BANKING": "NIFTY BANK",
    "FMCG": "NIFTY FMCG",
    "AUTO": "NIFTY AUTO",
    "METAL": "NIFTY METAL",
    "INFRA": "NIFTY INFRA",
    "REALTY": "NIFTY REALTY",
    "PSU BANK": "NIFTY PSU BANK",
}


def _resolve_nifty_sector_key(raw_sector: str, available_sector_keys: list[str]) -> str:
    normalized = (raw_sector or "").upper().strip()
    if not normalized:
        raise ValueError("Empty sector name from market data")

    mapped = SECTOR_TO_NIFTY_KEY.get(normalized)
    if mapped and mapped in available_sector_keys:
        return mapped

    direct_nifty = f"NIFTY {normalized}"
    if direct_nifty in available_sector_keys:
        return direct_nifty

    if normalized in available_sector_keys:
        return normalized

    for key in available_sector_keys:
        if normalized in key or key in normalized:
            return key

    raise ValueError(
        f"No matching NIFTY sector key for '{raw_sector}'. "
        f"Available keys: {', '.join(available_sector_keys)}"
    )

class DataFetcherCorrelation:
    @staticmethod
    def fetch_correlation_data(symbol):
        try:

            sector = get_sector_yf(symbol)
            if not sector:
                raise ValueError(f"Sector information not found for symbol: {symbol}")

            # First load with a valid default, then resolve the exact mapped key from
            # available sector columns to avoid yfinance-sector mismatch errors.
            nifty_series, sector_price_df, _ = get_nifty_and_sector_data("NIFTY BANK")
            available_sector_keys = [str(col) for col in sector_price_df.columns]
            resolved_sector_key = _resolve_nifty_sector_key(sector, available_sector_keys)
            stock_sector_series = sector_price_df[resolved_sector_key]

            if nifty_series is None or sector_price_df is None or stock_sector_series is None:
                raise ValueError("No Nifty and sector data found")
            
            if nifty_series.empty or sector_price_df.empty or stock_sector_series.empty:
                raise ValueError("Nifty and sector data is empty")
            
            stock_series_data = get_stock_series(symbol)
            if stock_series_data is None or stock_series_data.empty:
                raise ValueError("No stock series data found for the given symbols")
            
            return {
                "nifty_series": nifty_series,
                "sector_price_df": sector_price_df,
                "stock_series": stock_series_data,
                "stock_sector_series": stock_sector_series,
                "resolved_sector_key": resolved_sector_key,
            }
        except Exception as e:
            raise ValueError(f"Error fetching correlation data: {str(e)}")