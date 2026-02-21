from agents.StockAgent import StockAgent
from agents.StockSignal import StockSignal
from utilities.technical.build_technical_rationale import build_technical_rationale
import numpy as np


class TechnicalAgent(StockAgent):
    """
    Interprets technical indicators into a directional signal.
    """

    def __init__(self):
        super().__init__(name="technical", horizon="short")

    def compute_technical_deltas(self, indicators: dict) -> dict:
        """
        MCP: Convert indicators into normalized deltas.
        """

        close = indicators["price"]

        ema_delta = (close - indicators["EMA_50"]) / indicators["EMA_50"]
        upper_delta = (indicators["BB_upper"] - close) / close
        lower_delta = (close - indicators["BB_lower"]) / close

        return {
            "ema_delta": float(ema_delta),
            "upper_band_delta": float(upper_delta),
            "lower_band_delta": float(lower_delta),
        }

    def run(self, symbol: str, mcp_data: dict) -> StockSignal:
        technical_data = mcp_data["technicals"]

        deltas = self.compute_technical_deltas(technical_data)


        technical_score = technical_data["direction"] * technical_data["momentum"] * (1 - technical_data["BB_penalty"])

        delta_score = (
            0.5 * np.tanh(deltas["ema_delta"] * 10)
        )
        score = (technical_score + delta_score)/2

        confidence = min(1.0, abs(score))

        numeric_rationale = f"""
            EMA delta={deltas['ema_delta']:.3f}, 
            BB penalty={technical_data['BB_penalty']:.3f}, 
            momentum score={technical_data['momentum']:.3f}, 
            direction={technical_data['direction']:.3f}
        """

        structural_rationale = build_technical_rationale(technical_data)



        return StockSignal(
            symbol=symbol,
            agent=self.name,
            score=float(score),
            confidence=float(confidence),
            horizon=self.horizon,
            numeric_rationale=numeric_rationale,
            structural_rationale=structural_rationale,
            evidence= {**technical_data, **deltas}
        )
