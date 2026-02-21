import pickle
import faiss
from utilities.memory.validate_memory import validate_memory

def load_pattern_memory(path: str):

    with open(f"{path}/pca.pkl", "rb") as f:
        pca = pickle.load(f)

    index = faiss.read_index(f"{path}/index.faiss")

    with open(f"{path}/meta.pkl", "rb") as f:
        meta = pickle.load(f)

    # NEW → Load config if exists
    try:
        with open(f"{path}/config.pkl", "rb") as f:
            config = pickle.load(f)
    except FileNotFoundError:
        config = {"version": 0}

    memory = {
        "pca": pca,
        "index": index,
        "meta": meta,
        "config": config
    }

    validate_memory(memory)

    return memory
