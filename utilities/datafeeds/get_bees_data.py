from utilities.datafeeds.get_ticket_history_week import get_ticker_history_week


def get_bees_data():
  bees_data = {}
  goldbees_data = get_ticker_history_week("GOLDBEES.NS")
  goldbees_data = goldbees_data[["Open","High","Low","Close"]]
  goldbees_data.reset_index(inplace=True)
  goldbees_data.drop("Date", axis=1, inplace=True)
  bees_data["GOLDBEES"] = goldbees_data
  goldbees_data = get_ticker_history_week("SILVERBEES.NS")
  goldbees_data = goldbees_data[["Open","High","Low","Close"]]
  goldbees_data.reset_index(inplace=True)
  goldbees_data.drop("Date",axis=1, inplace=True)
  bees_data["SILVERBEES"] = goldbees_data

  return bees_data