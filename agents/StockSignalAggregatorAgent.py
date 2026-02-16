import numpy as np
from typing import List
from agents.StockAgent import StockAgent

class StockSignalAggregator:
    """
    Decision Authority:
    - Calls stock agents
    - Consumes RegimeSignal
    - Aggregates signals
    """

    def __init__(self, stock_agents: List[StockAgent]):
        self.stock_agents = stock_agents

    def run(self, symbol: str, mcp_data: dict, regime_signal) -> dict:
        """
        symbol → stock ticker
        mcp_data → precomputed MCP outputs (unchanged)
        regime_signal → output of RegimeAgent (unchanged)
        """

        signals = []

        # ---- CALL OTHER AGENTS (NEW BEHAVIOR) ----
        for agent in self.stock_agents:
            signals.append(agent.run(symbol, mcp_data))

        # ---- ORIGINAL AGGREGATION LOGIC (UNCHANGED) ----
        if not signals:
            return {
                "final_score": 0.0,
                "confidence": 0.0,
                "regime": "NA",
                "disagreement": 0.0,
                "signals": [],
                "evidence": {}
            }

        scores = np.array([s.score for s in signals])
        confidences = np.array([s.confidence for s in signals])

        evidence = {s.__class__.__name__: s.evidence for s in signals}

        weighted_score = np.sum(scores * confidences) / (np.sum(confidences) + 1e-8)
        disagreement = np.std(scores)
        regime = regime_signal.regime

        return {
            "final_score": float(weighted_score),
            "confidence": float(np.mean(confidences)),
            "disagreement": float(disagreement),
            "signals": signals,
            "regime": regime,
            "evidence": evidence
        }
