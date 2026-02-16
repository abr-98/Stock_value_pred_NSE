from utilites.portfolio.rolling_corr_matrix import rolling_corr_matrix

def avg_pairwise_corr(returns, window=60):
    rolling = rolling_corr_matrix(returns, window)
    avg_corr = rolling.groupby(level=0).mean().mean(axis=1)
    return avg_corr
