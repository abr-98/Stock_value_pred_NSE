from utilities.datafeeds.get_ticket_history_week import get_ticker_history_week
from utilities.datafeeds.create_dataframe import create_dataframe
from utilities.datafeeds.make_lstm_sequences import make_lstm_sequences


def get_nifty_50(models):
  data = get_ticker_history_week("^NSEI")
  data = data.reset_index()
  data = data[["Open", "High","Low","Close"]]
  nifty_df = data
  nifty_df_mod = create_dataframe(nifty_df, nselib=True)

  # Feature matrix
  FEATURE_COLS = [
      "RSI", "MACD", "Upper", "Mid", "Lower",
      "EMA_50", "EMA_200", "ATR", "ADX"
  ]

  nifty_X = make_lstm_sequences(nifty_df_mod, FEATURE_COLS)

  nifty_model = models["NIFTY 50"]
  return nifty_df, nifty_X, nifty_model
