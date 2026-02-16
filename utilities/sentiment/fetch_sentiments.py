from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def headline_sentiment(headline: str) -> dict:
  analyzer = SentimentIntensityAnalyzer()
  sentiment = analyzer.polarity_scores(headline)
  return sentiment