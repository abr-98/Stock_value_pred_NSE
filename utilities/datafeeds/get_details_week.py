from nselib import capital_market
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_details_week(sector):
  to_date = datetime.today() - timedelta(days=1)

  # 10 years before yesterday
  from_date = to_date - relativedelta(days=10)

  # Format dates as DD-MM-YYYY
  to_date_str = to_date.strftime("%d-%m-%Y")
  from_date_str = from_date.strftime("%d-%m-%Y")
  try:
    sector_data = capital_market.index_data(
        index=sector,
        from_date=from_date_str,
        to_date=to_date_str
    )
    sector_data = sector_data[["OPEN_INDEX_VAL","HIGH_INDEX_VAL","CLOSE_INDEX_VAL","LOW_INDEX_VAL"]]
    sector_data.rename(columns={"OPEN_INDEX_VAL":"Open","HIGH_INDEX_VAL":"High","CLOSE_INDEX_VAL":"Close","LOW_INDEX_VAL":"Low"},inplace=True)
    return sector_data
  except:
    return None
