import numpy as np
import pandas as pd
from utilities.portfolio.build_price_matrix import build_price_matrix

def portfolio_risk_agent(history_dict):

    prices = build_price_matrix(history_dict)
    weights_dict = history_dict["weights"]

    weights = np.array([weights_dict[t] for t in prices.columns])

    # -------------------------
    # 1️⃣ Returns
    # -------------------------
    rets = prices.pct_change().dropna()

    # -------------------------
    # 2️⃣ Covariance Risk (True portfolio risk)
    # -------------------------
    cov_matrix = rets.cov().values

    port_var = weights.T @ cov_matrix @ weights
    port_vol_daily = np.sqrt(port_var)

    annual_vol = port_vol_daily * np.sqrt(252)

    # -------------------------
    # 3️⃣ Tail Risk (CVaR)
    # -------------------------
    port_rets = rets @ weights

    alpha = 0.05
    var_cutoff = np.percentile(port_rets, alpha * 100)
    cvar_value = port_rets[port_rets <= var_cutoff].mean()

    # -------------------------
    # 4️⃣ Diversification Quality
    # -------------------------
    weighted_vol = np.sum(rets.std().values * weights) * np.sqrt(252)
    diversification_ratio = weighted_vol / annual_vol

    # -------------------------
    # 5️⃣ Stable Risk Score
    # -------------------------
    risk_score = np.tanh(annual_vol / 0.25) * 100

    # -------------------------
    # 6️⃣ Confidence Score
    # -------------------------
    confidence = np.clip(50 * diversification_ratio, 0, 100)

    return {
        "annual_volatility": round(float(annual_vol), 4),
        "cvar": round(float(cvar_value), 4),
        "diversification_ratio": round(float(diversification_ratio), 3),
        "risk_score": round(float(risk_score), 2),
        "confidence": round(float(confidence), 2)
    }
