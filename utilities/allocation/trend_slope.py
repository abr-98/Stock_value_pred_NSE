import numpy as np

def trend_slope(window):
    y = window["Close"].values
    x = np.arange(len(y))

    slope = np.polyfit(x, y, 1)[0]
    return slope / y.mean()
