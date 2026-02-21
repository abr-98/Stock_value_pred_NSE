import faiss
import numpy as np

def build_faiss_index(vectors):

    vectors = vectors.astype("float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)   # exact search, deterministic

    index.add(vectors)

    return index