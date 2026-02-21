from utilities.explaination.get_indicators import get_indicators
from utilities.explaination.compute_trend_strength_series import compute_trend_strength_series
from utilities.explaination.distance_from_range import distance_from_range_series
from utilities.explaination.get_volume_ratio import get_volume_ratio
from utilities.explaination.get_spread import get_spread
from utilities.explaination.get_regime import get_regime
import pandas as pd


def create_final_dataframe(df):
    df = get_indicators(df)
    df["trend_strength"] = compute_trend_strength_series(df)
    df["distance_from_range"] = distance_from_range_series(df)
    df = get_spread(df)
    df = get_regime(df)
    df = get_volume_ratio(df)

    df.dropna(inplace=True)

    df["entry_signal"] = (df["trend_strength"] > 0.5).astype(int)
    trade_rows = df[df["entry_signal"] == 1].copy()

    holding_period = 5

    trade_rows["future_return"] = (
        df["Close"].shift(-holding_period) - df["Close"]
    ) / df["atr"]

    trade_rows["realized_R"] = trade_rows["future_return"]

    trade_rows.drop(["Date", "Close","Open","High","Low","Volume","returns","entry_signal","range","atr","future_return"], axis=1, inplace=True)

    df_dummies = pd.get_dummies(trade_rows[["regime","spread_state"]],dtype=int)
    final_df = pd.concat([trade_rows.drop(["regime","spread_state"], axis=1), df_dummies], axis=1)


    return final_df