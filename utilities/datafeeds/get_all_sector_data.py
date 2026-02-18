from utilites.datafeeds.get_bees_data import get_bees_data
from utilites.datafeeds.get_sector_data import get_sector_data

def get_all_sector_data():
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
  bees_data = get_bees_data()
  sector_data = get_sector_data(sectors)
  sector_data.update(bees_data)
  return sector_data

