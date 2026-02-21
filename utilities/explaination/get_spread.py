import numpy as np

def get_spread(df):
    df["spread_state"] = np.where(
    df["range"] / df["atr"] > 1.5, "WIDE", "NORMAL"
) 
    return df