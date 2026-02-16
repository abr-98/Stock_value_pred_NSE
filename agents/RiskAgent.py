from agents import StockAgent
from agents.StockSignal import StockSignal
import numpy as np


class RiskAgent(StockAgent):
    """
    Interprets news / social sentiment.
    """

    def __init__(self):
        super().__init__(name="risk", horizon="short")

    def run(self, symbol: str, mcp_data: dict) -> StockSignal:
        risk_data = mcp_data["risk"]

        atr_pct=risk_data["ATR_pct"]
        vol=risk_data["volatility"]
        dd=risk_data["max_drawdown"]
        cvar_value=risk_data["cvar"]

        atr_risk  = np.tanh(atr_pct / 0.05)
        vol_risk  = np.tanh(vol / 0.04)
        dd_risk   = np.tanh(dd / 0.3)
        cvar_risk  = np.tanh(abs(cvar_value) / 0.05)

        risk_score = (
            atr_risk * 0.25 +
            vol_risk * 0.25 +
            dd_risk  * 0.20 +
            cvar_risk * 0.30      # Tail risk deserves highest weight
        ) * 100


        confidence = 100 * np.exp(-risk_score / 70)

        rationale = (
            f"ATR pct={atr_pct:.3f}",
            f"Volatility={vol:.3f}",
            f"Max drawdown={dd:.3f}",
            f"CVAR ={cvar_value:.3f}"
        )

        return StockSignal(
            symbol=symbol,
            agent=self.name,
            score=float(risk_score),
            confidence=float(confidence),
            horizon=self.horizon,
            rationale=rationale,
            evidence=risk_data
        )
