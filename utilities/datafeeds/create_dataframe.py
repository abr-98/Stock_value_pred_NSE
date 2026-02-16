from utilites.datafeeds.add_technical_indicators import add_technical_indicators
from utilites.datafeeds.add_regime_indicator import add_regime_indicators


def create_dataframe(history, nselib =False):

  FEATURE_COLS = [
    "RSI", "MACD", "Upper", "Mid", "Lower",
    "EMA_50", "EMA_200", "ATR", "ADX"]
  df = add_technical_indicators(history)
  df = add_regime_indicators(df)
  df = df.dropna()
  if not nselib:
    df = df.reset_index().drop(["Date"], axis=1)
    df = df.drop(["Volume","Dividends","Stock Splits"], axis=1)

  #df = decompose_price(df)

  #df = build_residual_target(df, horizon=10)
  df = df.drop(["Open","High","Low","Close"], axis=1)
  #print(df.head())
  df = df.dropna()
  #df[FEATURE_COLS] = (
    #df[FEATURE_COLS] - df[FEATURE_COLS].mean()) / (df[FEATURE_COLS].std() + 1e-9)

  df.dropna(inplace=True)
  return df

