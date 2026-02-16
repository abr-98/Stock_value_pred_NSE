from utilites.model_utilities.make_feature_names import make_feature_names


def return_feature_names():
  FEATURE_COLS = [
    "RSI", "MACD", "Upper", "Mid", "Lower",
    "EMA_50", "EMA_200", "ATR", "ADX"
  ] 
  feature_names = make_feature_names(FEATURE_COLS, seq_len=7)
  return feature_names