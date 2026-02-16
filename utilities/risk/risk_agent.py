from utilites.risk.returns import returns
from utilites.risk.max_drawdown import max_drawdown
from utilites.risk.rolling_volatility import rolling_volatility
import pandas as pd


def risk_agent(df):
    """
    df must contain: ['Close', 'High', 'Low']
    """

    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    # -------------------------
    # 1️⃣ Volatility risk (ATR)
    # -------------------------
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(14).mean().iloc[-1]
    atr_pct = atr / close.iloc[-1]

    # Normalize ATR risk
    atr_risk = min(atr_pct / 0.05, 1.0)  # 5% = high risk

    # -------------------------
    # 2️⃣ Volatility instability
    # -------------------------
    rets = returns(close)
    vol = rolling_volatility(rets).iloc[-1]
    vol_risk = min(vol / 0.04, 1.0)  # 4% daily vol = risky

    # -------------------------
    # 3️⃣ Drawdown risk
    # -------------------------
    dd = abs(max_drawdown(close))
    dd_risk = min(dd / 0.3, 1.0)  # 30% drawdown = severe

    cvar = cvar(returns(close))

    return {
            "ATR_pct": round(atr_pct * 100, 2),
            "volatility": round(vol * 100, 2),
            "max_drawdown": round(dd * 100, 2),
            "cvar": round(cvar,2)
          }