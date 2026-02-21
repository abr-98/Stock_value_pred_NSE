
def get_indicators(df):
  df["returns"] = df["Close"].pct_change()
  df["range"] = df["High"] - df["Low"]
  df["atr"] = df["range"].rolling(14, min_periods=1).mean()
  df["volatility"] = df["returns"].rolling(14, min_periods=1).std()

  return df
