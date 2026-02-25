import numpy as np
import logging

logger = logging.getLogger(__name__)

def make_lstm_sequences(df, feature_cols, seq_len=7):
    X = []

    values = df[feature_cols].values

    n_features = len(feature_cols)
    n_rows = len(values)

    if n_rows == 0:
        logger.warning(
            "make_lstm_sequences received empty input; returning zero-padded sequence (seq_len=%s, n_features=%s)",
            seq_len,
            n_features,
        )
        return np.zeros((seq_len, n_features), dtype=np.float32)

    if n_rows < seq_len:
        pad_len = seq_len - n_rows
        logger.warning(
            "make_lstm_sequences received short input (rows=%s < seq_len=%s); left-padding %s rows",
            n_rows,
            seq_len,
            pad_len,
        )
        pad_block = np.repeat(values[:1], pad_len, axis=0)
        padded_values = np.vstack([pad_block, values])
        return np.array(padded_values, dtype=np.float32)

    for i in range(len(values) - seq_len + 1):
        X.append(values[i:i + seq_len])

    return np.array(X[-1], dtype=np.float32)