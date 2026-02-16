

def make_feature_names(feature_cols, seq_len):
    names = []
    for t in range(seq_len):
        for f in feature_cols:
            names.append(f"{f}_t-{seq_len - t}")
    return names