def classify_sector_regime(avg_sector_corr, high_thresh=0.7, low_thresh=0.4):

    # Convert Series → scalar safely
    if hasattr(avg_sector_corr, "iloc"):
        avg_sector_corr = float(avg_sector_corr.iloc[-1])

    if avg_sector_corr >= high_thresh:
        return "SYSTEMIC"
    elif avg_sector_corr <= low_thresh:
        return "ROTATION"
    else:
        return "MIXED"
