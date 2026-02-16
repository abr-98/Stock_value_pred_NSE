def build_price_matrix(history_dict):
    import pandas as pd

    prices_df = pd.DataFrame(history_dict["prices"])
    prices_df = prices_df.dropna()  # ensure aligned window

    return prices_df