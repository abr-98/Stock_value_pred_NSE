from utilites.correlation.classify_nifty_regime import classify_nifty_regime
from utilites.correlation.stock_sector_correlation import stock_sector_correlation
from utilites.correlation.classify_sector_regime import classify_sector_regime
from utilites.correlation.correlation_based_profile import correlation_based_profile
from utilites.correlation.average_sector_correlation import average_sector_correlation
from utilites.serialization_helper import convert_to_serializable


def market_structure_agent(nifty_series, sector_price_df, stock_series, stock_sector_series):

    nifty_regime = classify_nifty_regime(nifty_series)

    avg_sector_corr = average_sector_correlation(sector_price_df)
    sector_regime = classify_sector_regime(avg_sector_corr)

    ss_corr = stock_sector_correlation(stock_series, stock_sector_series)

    profile = correlation_based_profile(
        nifty_regime,
        sector_regime,
        ss_corr
    )

    result = {
        "nifty_regime": nifty_regime,
        "avg_sector_corr": round(avg_sector_corr, 3),
        "sector_regime": sector_regime,
        **profile
    }
    
    # Convert all numpy/pandas types to Python native types
    return convert_to_serializable(result)
