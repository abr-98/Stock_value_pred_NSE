def validate_memory(memory):

    index_dim = memory["index"].d
    pca_dim = memory["pca"].n_components_

    if index_dim != pca_dim:
        raise ValueError(
            f"Dimension mismatch → FAISS({index_dim}) vs PCA({pca_dim})"
        )

    if len(memory["meta"]) != memory["index"].ntotal:
        raise ValueError(
            "Metadata size mismatch → vectors and metadata misaligned"
        )