def max_drawdown(close, window=120):
    roll_max = close.rolling(window,min_periods= 1).max()
    drawdown = (close - roll_max) / roll_max
    return drawdown.min()