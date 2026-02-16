def returns(close):
    return close.pct_change().dropna()