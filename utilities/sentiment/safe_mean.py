import numpy as np

def safe_mean(values):
    return float(np.mean(values)) if len(values) else 0.0