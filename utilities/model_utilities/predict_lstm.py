import torch

def predict_lstm(model, X_seq, device="cpu"):
    model.eval()
    with torch.no_grad():
        x = torch.tensor([X_seq], dtype=torch.float32).unsqueeze(0).to(device)
        return model(x).item()