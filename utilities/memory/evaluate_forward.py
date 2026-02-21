import numpy as np

def evaluate_forward(prices, meta, matched_indices, horizon=20):

    outcomes = []

    for idx in matched_indices:

        hist_i = meta[idx]["index"]

        if hist_i + horizon >= len(prices):
            continue

        ret = np.log(prices[hist_i + horizon] / prices[hist_i])
        outcomes.append(ret)

    return np.array(outcomes)
