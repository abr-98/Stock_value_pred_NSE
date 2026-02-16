from utilites.portfolio.log_returns import log_returns
from utilites.portfolio.avg_pairwise_corr import avg_pairwise_corr, effective_number_of_bets, variance_contribution
from utilites.portfolio.pairwise_correlation import pairwise_correlation
from utilites.portfolio.correlation_regime import correlation_regime
from utilites.portfolio.risk_agent import portfolio_risk_agent
import pandas as pd

def correlation_agent(data: dict):
    returns = pd.DataFrame({
        k: log_returns(v) for k, v in data["prices"].items()
    }).dropna()

    corr = returns.corr()
    avg_corr = avg_pairwise_corr(returns)
    enb = effective_number_of_bets(corr)
    var_conc = variance_contribution(corr)

    #groupwise_analyis = hierarchical_diversification_agent(data["prices"], data["weights"], data["sector_map"], data["industry_map"])

    full_analysis=  {
        "pairwise_corr": pairwise_correlation(returns),
        "avg_correlation": avg_corr.iloc[-1],
        "avg_correlation_trend": avg_corr.iloc[-1] - avg_corr.iloc[-20],
        "effective_bets": enb,
        "variance_concentration": var_conc,
        "correlation_regime": correlation_regime(avg_corr)
    }
    #full_analysis.update(groupwise_analyis)
    full_analysis.update(portfolio_risk_agent(data))

    return full_analysis