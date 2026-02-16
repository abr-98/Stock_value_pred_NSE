from lime.lime_tabular import LimeTabularExplainer
import numpy as np
from utilites.model_utilities.lstm_predict_wrapper import lstm_predict_wrapper

def explain_lstm_instance(
    model,
    X_seq,              # shape: (7, 9)
    feature_names,      # length = 9
    seq_len=7,
    n_features=9,
    device="cpu",
    num_samples=500,
    num_features_to_show=10
):
    X_flat = X_seq.reshape(-1)

    training_data = np.random.normal(
        loc=X_flat,
        scale=0.01,
        size=(num_samples, X_flat.shape[0])
    )

    lime_feature_names = [
        f"t{t}_{f}"
        for t in range(seq_len)
        for f in feature_names
    ]

    explainer = LimeTabularExplainer(
        training_data=training_data,
        feature_names=lime_feature_names,
        mode="regression",
        discretize_continuous=True,
        verbose=False
    )

    explanation = explainer.explain_instance(
        data_row=X_flat,
        predict_fn=lstm_predict_wrapper(
            model,
            seq_len=seq_len,
            n_features=n_features,
            device=device
        ),
        num_features=num_features_to_show
    )

    return explanation
