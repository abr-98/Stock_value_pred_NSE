from utilities.datafeeds.get_details_week import get_details_week

def get_sector_data(sectors):
  sector_data = {}
  for sector in sectors:
    sector_data[sector] = get_details_week(sector)
  return sector_data