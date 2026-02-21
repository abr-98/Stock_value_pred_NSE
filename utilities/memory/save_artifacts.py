import os
import pickle
import faiss

def save_artifacts(memory: dict, path: str):

    os.makedirs(path, exist_ok=True)

    with open(f"{path}/pca.pkl", "wb") as f:
        pickle.dump(memory["pca"], f)

    faiss.write_index(memory["index"], f"{path}/index.faiss")

    with open(f"{path}/meta.pkl", "wb") as f:
        pickle.dump(memory["meta"], f)

    # NEW → Store schema / config
    config = {
        "version": 1,
        "window": memory.get("window"),
        "feature_names": memory.get("feature_names"),
    }

    with open(f"{path}/config.pkl", "wb") as f:
        pickle.dump(config, f)
