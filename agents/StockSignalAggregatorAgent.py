import numpy as np

class StockSignalAggregatorAgent:

    def __init__(self, stock_agents):
        self.stock_agents = stock_agents

    def run(self, symbol: str, mcp_data: dict, regime_signal) -> dict:

        signals = []

        for agent in self.stock_agents:
            if not agent.name == "regime_stock":
                signals.append(agent.run(symbol, mcp_data))

        if not signals:
            return {
                "final_score": 0.0,
                "confidence": 0.0,
                "regime": "NA",
                "disagreement": 0.0,
                "signals": [],
                "numeric_rationale": "",
                "structural_rationale": "",
                "meta_rationale": "",
                "evidence": {}
            }

        scores = np.array([s.score for s in signals])
        confidences = np.array([s.confidence for s in signals])

        weighted_score = np.sum(scores * confidences) / (np.sum(confidences) + 1e-8)
        disagreement = np.std(scores)

        # =====================================================
        # EVIDENCE MERGING (SAFE)
        # =====================================================

        evidence = {s.agent: s.evidence for s in signals}

        # =====================================================
        # RATIONALE AGGREGATION
        # =====================================================

        numeric_rationales = []
        structural_rationales = []

        for s in signals:

            numeric_rationales.append(s.numeric_rationale)

            if s.structural_rationale:
                structural_rationales.append(s.structural_rationale)

        numeric_rationale = " | ".join(numeric_rationales)
        structural_rationale = " | ".join(structural_rationales)

        # =====================================================
        # META-LEVEL RATIONALE (VERY IMPORTANT)
        # =====================================================

        meta_rationale_parts = []

        if disagreement > 0.5:
            meta_rationale_parts.append("High agent disagreement → Conviction fragile")

        elif disagreement < 0.15:
            meta_rationale_parts.append("Low agent disagreement → Signal alignment strong")

        meta_rationale_parts.append(f"Market regime = {regime_signal.regime}")

        meta_rationale = " | ".join(meta_rationale_parts)

        return {
            "final_score": float(weighted_score),
            "confidence": float(np.mean(confidences)),
            "disagreement": float(disagreement),
            "signals": signals,
            "regime": regime_signal.regime,
            "numeric_rationale": numeric_rationale,
            "structural_rationale": structural_rationale,
            "meta_rationale": meta_rationale,
            "evidence": evidence,
        }
