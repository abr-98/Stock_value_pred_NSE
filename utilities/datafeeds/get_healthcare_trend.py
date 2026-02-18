from utilites.datafeeds.yfinance_config import yf
import pandas as pd
from utilites.technical.rsi import rsi
from utilites.technical.ema import ema

def get_healthcare_trend():
  stocks = ["SUNPHARMA.NS", "APOLLOHOSP.NS", "DRREDDY.NS", "DIVISLAB.NS", "CIPLA.NS"]

  data = yf.download(
      stocks,
      period="2mo",
      interval="1d",
      group_by="ticker",
      auto_adjust=True,
      progress=False
  )
  close_df = pd.DataFrame({
      stock: data[stock]["Close"]
      for stock in stocks
  })
  returns = close_df.pct_change()
  returns["NIFTY_HEALTHCARE_SYNTH"] = returns.mean(axis=1)
  index_price = 1000 * (1 + returns["NIFTY_HEALTHCARE_SYNTH"]).cumprod()
  index_price.dropna(inplace=True)
  nifty_oilgas_df = pd.DataFrame({
      "Close": index_price
  })
  nifty_oilgas_df["RSI"] = rsi(nifty_oilgas_df["Close"])
  nifty_oilgas_df["EMA_50"] = ema(nifty_oilgas_df["Close"], 50)
  nifty_oilgas_df["EMA_200"] = ema(nifty_oilgas_df["Close"], 200)
  nifty_oilgas_df.dropna(inplace=True)
  return nifty_oilgas_df