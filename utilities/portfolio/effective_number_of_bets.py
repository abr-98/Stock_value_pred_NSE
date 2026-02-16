import numpy as np
import pandas as pd

def effective_number_of_bets(corr: pd.DataFrame):
    eigenvals = np.linalg.eigvals(corr)
    eigenvals = eigenvals[eigenvals > 0]
    return (eigenvals.sum() ** 2) / (np.square(eigenvals).sum())
