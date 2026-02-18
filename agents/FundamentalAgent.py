from agents.StockAgent import StockAgent
from agents.StockSignal import StockSignal
import numpy as np
from utilites.fundamental.build_fundamental_rationale import build_fundamental_rationale

class FundamentalAgent(StockAgent):
    """
    Interprets financial fundamentals.
    """

    def __init__(self):
        super().__init__(name="fundamental", horizon="long")

    def run(self, symbol: str, mcp_data: dict) -> StockSignal:
        fundamentals = mcp_data["fundamentals"]

        score = score = np.tanh(
            fundamentals.get("roe", 0) * 2.0
            + fundamentals.get("revenue_growth", 0) * 1.5
            + fundamentals.get("revenue_yoy", 0) * 1.5
            + fundamentals.get("altman_z", 0) * 1.0
            - fundamentals.get("pe", 0) * 0.05
        )


        confidence = 0.7  # typically slower-moving

        rationale = (
            f"ROE={fundamentals.get('roe')}, "
            f"Revenue growth={fundamentals.get('revenue_growth')}"
            f"Revenue YOY={fundamentals.get('revenue_yoy')}"
            f"ALTMAN Z={fundamentals.get('altman_z')}"
            f"PE={fundamentals.get('pe')}"
        )
        structural_rationale = build_fundamental_rationale(fundamentals)

        return StockSignal(
            symbol=symbol,
            agent=self.name,
            score=float(score),
            confidence=confidence,
            horizon=self.horizon,
            numeric_rationale=rationale,
            structural_rationale=structural_rationale,
            evidence=fundamentals
        )
