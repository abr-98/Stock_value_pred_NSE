import numpy as np

def average_sector_correlation(sector_prices, window=30):
    returns = sector_prices.pct_change()

    corr_matrix = returns.rolling(window, min_periods=1).corr()

    # Extract latest correlation block
    latest_corr = corr_matrix.iloc[-len(sector_prices.columns):]

    # Remove self-correlations (diagonal = 1)
    values = latest_corr.values
    off_diag = values[values < 0.999]

    return np.nanmean(off_diag)
