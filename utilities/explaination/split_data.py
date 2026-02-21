def get_split_data(trade_rows):

    y = trade_rows["realized_R"]
    X = trade_rows.drop(["realized_R"], axis=1)

    return X, y
    