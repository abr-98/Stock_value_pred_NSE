import torch
from utilites.model_utilities.lstm_model import ResidualLSTM

def load_models(sectors, device="cpu"):
    models = {}
    for sector in sectors:
        model = ResidualLSTM(input_dim=9, hidden_dim=32)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model.to(device)

        try:
          model.load_state_dict(torch.load(f"/models/best_lstm_return_model_{sector}.pt", map_location=device))

          model.to(device)
          model.eval()
          models[sector] = model
        except:
          models[sector] = None
    return models
