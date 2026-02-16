from agents.StockAgent import BaseAgent
from agents.RegimeSignal import RegimeSignal


class RegimeStockAgent(BaseAgent):
    """
    Interprets technical indicators into a directional signal.
    """

    def __init__(self):
        super().__init__(name="regime_stock", horizon="short")


    def run(self, symbol: str, mcp_data: dict) -> RegimeSignal:
        regime_stock_data = mcp_data["regime_stock"]

        confidence = regime_stock_data["confidence"]
        score = regime_stock_data["score"]

        rationale = (
            f"ADX={regime_stock_data['ADX']:.3f}, "
            f"ATR_pct={regime_stock_data['ATR_pct']:.3f}"
        )

        return RegimeSignal(
            regime=regime_stock_data,
            confidence=confidence,
            sector_bias=None,
            rationale=rationale)
