from utilities.memory.compute_features_from_yf import compute_features_from_yf
from utilities.memory.transform_vector import transform_vector
from utilities.memory.query_similar import query_similar
from utilities.memory.evaluate_forward import evaluate_forward
import numpy as np


def query_current_state(df, memory, window=20, k=10, horizon=20):

    features = compute_features_from_yf(df)

    # Build current state vector
    current_vec = features.iloc[-window:].values.flatten()

    reduced_vec = transform_vector(memory["pca"], current_vec)

    idxs, dists = query_similar(memory["index"], reduced_vec, k)

    prices = features["price"].values

    forward = evaluate_forward(prices, memory["meta"], idxs, horizon=horizon)

    # Extract matched historical context (NEW)
    matches = []
    for idx, dist in zip(idxs, dists):

        meta_row = memory["meta"][idx]

        matches.append({
            "date": meta_row["date"],
            "distance": float(dist),
            "features": meta_row.get("features", {})
        })

    return {
        "matches": len(forward),

        "avg_forward_return": float(np.mean(forward)) if len(forward) else np.nan,

        "positive_ratio": float(np.mean(forward > 0)) if len(forward) else np.nan,

        "distance_stats": {
            "min": float(np.min(dists)) if len(dists) else np.nan,
            "max": float(np.max(dists)) if len(dists) else np.nan,
            "mean": float(np.mean(dists)) if len(dists) else np.nan,
        },

        "matched_instances": matches
    }
