def is_informative_window(window_df):

    vol = window_df["vol_20"].iloc[-1]
    ret = window_df["r_5"].iloc[-1]
    vol_z = window_df["volume_z"].iloc[-1]

    conditions = [
        abs(ret) > 0.03,        # strong move
        vol > window_df["vol_20"].median() * 1.5,
        abs(vol_z) > 2,         # volume shock
    ]

    return any(conditions)
