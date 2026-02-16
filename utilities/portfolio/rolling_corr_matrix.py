import pandas as pd

def rolling_corr_matrix(returns: pd.DataFrame, window=60):
    return returns.rolling(window).corr()