def stock_sector_correlation(stock, sector, window=30):

    stock = stock.squeeze()
    sector = sector.squeeze()

    r_stock = stock.pct_change()
    r_sector = sector.pct_change()

    aligned = r_stock.align(r_sector, join="inner")

    r_stock, r_sector = aligned

    return r_stock.rolling(window, min_periods=1).corr(r_sector)
