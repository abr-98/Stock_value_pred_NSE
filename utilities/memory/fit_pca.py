from sklearn.decomposition import PCA

def fit_pca(vectors, variance_target=0.9):

    pca = PCA(n_components=variance_target, svd_solver="full")
    reduced = pca.fit_transform(vectors)

    return pca, reduced