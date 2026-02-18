from agents.StockAgent import BaseAgent
from agents.RegimeSignal import RegimeSignal
from utilites.regime.build_regime_rationale import build_regime_rationale


class RegimeStockAgent(BaseAgent):
    """
    Interprets technical indicators into a directional signal.
    """

    def __init__(self):
        super().__init__(name="regime_stock")


    def run(self, symbol: str, mcp_data: dict) -> RegimeSignal:
        regime_stock_data = mcp_data["regime_stock"]

        confidence = regime_stock_data["confidence"]

        rationale = f"""
            ADX={regime_stock_data['ADX']:.3f}, 
            ATR_pct={regime_stock_data['ATR_pct']:.3f}
        """
        structural_rationale = build_regime_rationale(regime_stock_data)

        return RegimeSignal(
            regime=regime_stock_data,
            confidence=confidence,
            sector_bias=None,
            numeric_rationale=rationale,
            structural_rationale=structural_rationale)
