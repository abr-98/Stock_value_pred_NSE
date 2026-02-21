import yfinance as yf

def get_value(symbol):
  df = yf.download(symbol, start="2010-01-01")
  df.columns = df.columns.droplevel(1)
  df = df.reset_index()
  return df
