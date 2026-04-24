import sys
import torch
import os
from utilities.model_utilities.lstm_model import ResidualLSTM

def load_models(sectors, device="cpu"):
    models = {}
    # Get the project root directory (2 levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(project_root, "models")
    
    for sector in sectors:
        model = ResidualLSTM(input_dim=9, hidden_dim=32)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model.to(device)

        try:
            model_path = os.path.join(models_dir, f"best_lstm_return_model_{sector}.pt")
            if not os.path.exists(model_path):
                print(f"Warning: Model file not found: {model_path}", file=sys.stderr)
                models[sector] = None
                continue
                
            model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
            model.to(device)
            model.eval()
            models[sector] = model
        except Exception as e:
            print(f"Error loading model for {sector}: {str(e)}", file=sys.stderr)
            models[sector] = None
    return models
