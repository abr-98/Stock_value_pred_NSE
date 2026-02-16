import numpy as np

def make_lstm_sequences(df, feature_cols, seq_len=7):
    X = []

    values = df[feature_cols].values
    #print(len(values))

    for i in range(len(values) - seq_len + 1):
        X.append(values[i:i + seq_len])

    return np.array(X[-1])