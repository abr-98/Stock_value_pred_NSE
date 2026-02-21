## current:

def build_current_vector(features, window=20):

    w = features.iloc[-window:]
    return w.values.flatten()
