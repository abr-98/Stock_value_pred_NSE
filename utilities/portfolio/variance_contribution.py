import numpy as np
import pandas as pd

def variance_contribution(corr: pd.DataFrame):
    eigenvals, eigenvecs = np.linalg.eig(corr)
    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]

    total = eigenvals.sum()
    return {
        "pc1_variance": eigenvals[0] / total,
        "top3_variance": eigenvals[:3].sum() / total
    }