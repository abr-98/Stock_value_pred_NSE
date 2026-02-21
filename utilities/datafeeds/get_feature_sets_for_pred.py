from utilities.datafeeds.create_dataframe import create_dataframe
from utilities.datafeeds.make_lstm_sequences import make_lstm_sequences

def get_feature_sets_for_pred(sector_data):
  feature_sets = {}
  data_sets= {}
  FEATURE_COLS = [
      "RSI", "MACD", "Upper", "Mid", "Lower",
      "EMA_50", "EMA_200", "ATR", "ADX"
  ]
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

  sectors.append("SILVERBEES")
  sectors.append("GOLDBEES")

  for sector in sectors:
    if sector_data[sector] is None:
      continue
    if sector in ["GOLDBEES","SILVERBEES"]:
      data_sets[sector] = sector_data[sector]
      #print(sector_data[sector].head())
      data_sector= create_dataframe(sector_data[sector],nselib=True)
      X = make_lstm_sequences(data_sector, FEATURE_COLS)

      feature_sets[sector] = X
    else:
      data_sets[sector] = sector_data[sector]
      data_sector= create_dataframe(sector_data[sector], nselib=True)
      X = make_lstm_sequences(data_sector, FEATURE_COLS)
      feature_sets[sector] = X

  return feature_sets, data_sets