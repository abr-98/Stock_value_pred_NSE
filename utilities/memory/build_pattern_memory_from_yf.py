from utilities.memory.compute_features_from_yf import compute_features_from_yf
from utilities.memory.build_informative_window import build_informative_windows
from utilities.memory.build_faiss_index import build_faiss_index
from utilities.memory.fit_pca import fit_pca

def build_pattern_memory_from_yf(df):

    features = compute_features_from_yf(df)

    vectors, meta = build_informative_windows(features)

    if len(vectors) == 0:
        raise ValueError("No informative windows detected")

    pca, reduced = fit_pca(vectors)

    index = build_faiss_index(reduced)

    return {
        "pca": pca,
        "index": index,
        "meta": meta,
        "features": features
    }
