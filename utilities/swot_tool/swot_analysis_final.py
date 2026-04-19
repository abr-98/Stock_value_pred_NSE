def swot_analysis_final(ticker):
    import yfinance as yf
    from .swot_absolute import swot_absolute
    from .get_nifty_sector_and_peers import get_nifty_sector_and_peers
    from .fetch_metrics import fetch_metrics
    from .add_percentile_scores import add_percentile_scores
    from .factor_scores import factor_scores
    from .swot_relative import swot_relative
    from .merge_swot import merge_swot

    stock = yf.Ticker(ticker)
    info = stock.info

    # --- Absolute SWOT ---
    swot_abs = swot_absolute(ticker)

    # --- Peer-based SWOT ---
    sector, peers = get_nifty_sector_and_peers(ticker)

    df = fetch_metrics(peers)
    df = add_percentile_scores(df)
    df = factor_scores(df)

    swot_rel = swot_relative(df, ticker)

    # --- Merge ---
    final_swot = merge_swot(swot_abs, swot_rel)

    return final_swot