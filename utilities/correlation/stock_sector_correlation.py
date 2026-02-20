import numpy as np
import pandas as pd

def stock_sector_correlation(stock, sector, window=30):

    stock = stock.squeeze()
    sector = sector.squeeze()

    r_stock = stock.pct_change()
    r_sector = sector.pct_change()

    r_stock, r_sector = r_stock.align(r_sector, join="inner", axis=0)

    corr_result = r_stock.rolling(window, min_periods=1).corr(r_sector)
    
    # Get the last valid correlation value and convert to Python float
    last_corr = corr_result.iloc[-1]
    
    # Handle Series or scalar
    if isinstance(last_corr, pd.Series):
        last_corr = last_corr.iloc[-1]
    
    return float(last_corr)
