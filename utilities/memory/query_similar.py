def query_similar(index, vec, k=20):

    distances, indices = index.search(vec, k)
    return indices[0], distances[0]