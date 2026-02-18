import torch
import os
from utilites.model_utilities.lstm_model import ResidualLSTM

def load_nifty_50(models):
    model_nifty_50 = ResidualLSTM(input_dim=9, hidden_dim=32)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Get the project root directory (2 levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(project_root, "models", "best_lstm_return_model.pt")
    
    model_nifty_50.to(device)
    
    try:
        if not os.path.exists(model_path):
            print(f"Warning: NIFTY 50 model file not found: {model_path}")
            models["NIFTY 50"] = None
            return models
            
        model_nifty_50.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
        model_nifty_50.eval()
        models["NIFTY 50"] = model_nifty_50
    except Exception as e:
        print(f"Error loading NIFTY 50 model: {str(e)}")
        models["NIFTY 50"] = None

    return models