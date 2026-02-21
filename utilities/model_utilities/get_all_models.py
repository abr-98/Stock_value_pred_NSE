from utilities.model_utilities.load_models import load_models
from utilities.model_utilities.load_nifty_50 import load_nifty_50
from utilities.model_utilities.lstm_model import ResidualLSTM

def get_all_models():
  model = ResidualLSTM(
    input_dim=9,
    hidden_dim=32,
  )
  sector_to_nselib = {
    "Bank": "NIFTY BANK",
    "Auto": "NIFTY AUTO",
    "Financial Services": "NIFTY FINANCIAL SERVICES",
    "FMCG": "NIFTY FMCG",
    "IT": "NIFTY IT",
    "Media": "NIFTY MEDIA",
    "Metal": "NIFTY METAL",
    "Pharma": "NIFTY PHARMA",
    "Realty": "NIFTY REALTY",
    "Private Bank": "NIFTY PRIVATE BANK",
    "PSU Bank": "NIFTY PSU BANK",
    "Consumer Durables": "NIFTY CONSUMER DURABLES",
    "Oil and Gas": "NIFTY ENERGY",
    "Healthcare": "NIFTY HEALTHCARE"
  }
  sectors = list(sector_to_nselib.values())
  models = load_models(sectors)
  models = load_nifty_50(models)
  models["SILVERBEES"] = None
  models["GOLDBEES"] = None 
  return models
  
  