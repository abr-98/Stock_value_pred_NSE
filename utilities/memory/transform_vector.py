def transform_vector(pca, vec):

    return pca.transform(vec.reshape(1, -1)).astype("float32")