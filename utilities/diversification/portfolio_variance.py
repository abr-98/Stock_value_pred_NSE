import numpy as np

def portfolio_variance(weights, cov):
    w = np.array([weights[a] for a in cov.index])
    return w.T @ cov.values @ w