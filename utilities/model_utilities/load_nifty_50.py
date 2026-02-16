import torch
from utilites.model_utilities.lstm_model import ResidualLSTM

def load_nifty_50(models):
  model_nifty_50 = ResidualLSTM(input_dim=9, hidden_dim=32)
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

  model_nifty_50.to(device)
  model_nifty_50.load_state_dict(torch.load(f"/content/best_lstm_return_model.pt", map_location=device))

  models["NIFTY 50"] = model_nifty_50

  return models