from agents.StockAgent import StockAgent
from agents.StockSignal import StockSignal
from utilites.sentiment.build_sentiment_rationale import build_sentiment_rationale


class SentimentAgent(StockAgent):
    """
    Interprets news / social sentiment.
    """

    def __init__(self):
        super().__init__(name="sentiment", horizon="short")

    def run(self, symbol: str, mcp_data: dict) -> StockSignal:
        sentiment = mcp_data["sentiment"]

        company_score = sentiment["company_sentiment"]
        national_score = sentiment["national_sentiment"]

        score = (company_score*0.7 + national_score*0.3)

        confidence = min(1.0, abs(score))

        rationale = f"""
            Company sentiment={company_score:.3f}, 
            National sentiment={national_score:.3f}
        """
        
        structural_rationale = build_sentiment_rationale(sentiment)

        return StockSignal(
            symbol=symbol,
            agent=self.name,
            score=float(score),
            confidence=float(confidence),
            horizon=self.horizon,
            numeric_rationale=rationale,
            structural_rationale=structural_rationale,
            evidence=sentiment
        )
