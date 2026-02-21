from utilities.datafeeds.get_healthcare_trend import get_healthcare_trend
from utilities.datafeeds.get_gas_and_oil_trend import get_gas_and_oil_trend


def get_feed_data(models, datasets, feature_sets):
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
  feed_data = {}

  for sector in sectors:
    sector_corrected = sector.replace("NIFTY ", "")
    feed_data[sector_corrected] = {}
    if sector in ["SILVERBEES","GOLDBEES"]:
      feed_data[sector_corrected]["df"] = datasets[sector]
    elif sector in ["NIFTY ENERGY","NIFTY HEALTHCARE"]:
      if sector == "NIFTY ENERGY":
        feed_data[sector_corrected]["df"] = get_gas_and_oil_trend()
      else:
        feed_data[sector_corrected]["df"] = get_healthcare_trend()
    else:
      feed_data[sector_corrected]["df"] = datasets[sector]
      feed_data[sector_corrected]["X"] = feature_sets[sector]
      feed_data[sector_corrected]["model"] = models[sector]
  return feed_data
