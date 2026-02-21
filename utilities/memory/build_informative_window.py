from utilities.memory.is_informative_window import is_informative_window
import numpy as np

def build_informative_windows(features, window=20):

    vectors = []
    metadata = []

    for i in range(window, len(features)):

        w = features.iloc[i-window:i]

        if not is_informative_window(w):
            continue

        vectors.append(w.values.flatten())

        row = features.iloc[i]

        metadata.append({
            "index": i,
            "date": features.index[i],
            "features": {
                "r_5": float(row["r_5"]),
                "r_20": float(row["r_20"]),
                "vol_20": float(row["vol_20"]),
                "drawdown_20": float(row["drawdown_20"]),
                "volume_z": float(row["volume_z"]),
            }
        })

    return np.array(vectors), metadata
