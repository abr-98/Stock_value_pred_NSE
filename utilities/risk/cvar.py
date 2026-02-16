import numpy as np

def cvar(returns, alpha=0.95):
    """
    returns: 1D array-like of returns (negative = loss)
    alpha: confidence level (e.g. 0.95)
    """
    returns = np.asarray(returns)
    returns = returns[~np.isnan(returns)]

    if len(returns) == 0:
        return np.nan

    losses = -returns
    var_threshold = np.quantile(losses, alpha)

    tail_losses = losses[losses >= var_threshold]

    if len(tail_losses) == 0:
        return np.nan

    return tail_losses.mean()
