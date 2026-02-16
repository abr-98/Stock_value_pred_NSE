def correlation_regime(avg_corr_series):
    recent = avg_corr_series.iloc[-20:].mean()
    long = avg_corr_series.iloc[-120:].mean()

    if recent > long + 0.1:
        return "correlation_rising"
    elif recent < long - 0.1:
        return "correlation_falling"
    return "stable"