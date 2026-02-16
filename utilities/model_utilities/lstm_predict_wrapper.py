import numpy as np
import torch

def lstm_predict_wrapper(model, seq_len, n_features, device="cpu"):
    def predict(X_flat):
        """
        X_flat: (n_samples, seq_len * n_features)
        """
        X_flat = np.asarray(X_flat)

        assert X_flat.ndim == 2, "LIME input must be 2D"
        assert X_flat.shape[1] == seq_len * n_features, (
            f"Expected {seq_len * n_features} features, "
            f"got {X_flat.shape[1]}"
        )

        n_samples = X_flat.shape[0]

        X_seq = X_flat.reshape(
            n_samples,
            seq_len,
            n_features
        )

        X_seq = torch.tensor(X_seq, dtype=torch.float32).to(device)

        model.eval()
        with torch.no_grad():
            preds = model(X_seq).cpu().numpy().reshape(-1)

        return preds

    return predict

