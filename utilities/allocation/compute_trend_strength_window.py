from utilites.allocation.trend_direction import trend_direction
from utilites.allocation.trend_persistence import trend_persistence
from utilites.allocation.trend_quality import trend_quality
from utilites.allocation.trend_slope import trend_slope


def compute_trend_strength_window(df, lookback=50):
    window = df.tail(lookback)

    score = 0.0

    # Direction
    if trend_direction(window):
        score += 1

    # Slope strength
    slope = trend_slope(window)
    if slope > 0.002:
        score += 1
    elif slope < -0.002:
        score -= 1

    # Persistence
    persistence = trend_persistence(window)
    if persistence > 0.65:
        score += 1
    elif persistence < 0.4:
        score -= 1

    # Quality
    quality = trend_quality(window)
    if quality > 0.5:
        score += 1
    elif quality < 0:
        score -= 1

    return score
