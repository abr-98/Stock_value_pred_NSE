from utilities.diversification.log_returns import log_returns
from utilities.portfolio.avg_pairwise_corr import avg_pairwise_corr
from utilities.portfolio.effective_number_of_bets import effective_number_of_bets
from utilities.portfolio.variance_contribution import variance_contribution
from utilities.portfolio.pairwise_correlation import pairwise_correlation
from utilities.portfolio.correlation_regime import correlation_regime
from utilities.portfolio.risk_agent import portfolio_risk_agent
from utilities.serialization_helper import convert_to_serializable
import pandas as pd

def correlation_agent(data: dict):
    returns = pd.DataFrame({
        k: log_returns(v) for k, v in data["prices"].items()
    }).dropna()

    corr = returns.corr()
    avg_corr = avg_pairwise_corr(returns)
    enb = effective_number_of_bets(corr)
    var_conc = variance_contribution(corr)
    recent = avg_corr.iloc[-1]
    past = avg_corr.iloc[-20] if len(avg_corr) > 20 else avg_corr.iloc[0]

    #groupwise_analyis = hierarchical_diversification_agent(data["prices"], data["weights"], data["sector_map"], data["industry_map"])

    full_analysis=  {
        "pairwise_corr": pairwise_correlation(returns),
        "avg_correlation": recent,
        "avg_correlation_trend": recent - past,
        "effective_bets": enb,
        "variance_concentration": var_conc,
        "correlation_regime": correlation_regime(avg_corr)
    }
    #full_analysis.update(groupwise_analyis)
    full_analysis.update(portfolio_risk_agent(data))

    # Convert all numpy/pandas types to Python native types for JSON serialization
    return convert_to_serializable(full_analysis)