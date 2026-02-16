from utilites.sentiment.get_news_company import get_news_company
from utilites.sentiment.get_news_national import get_news_national
from utilites.sentiment.fetch_sentiments import headline_sentiment
import numpy as np

def get_sentiment(ticker):
  sentiment_company = get_news_company(ticker)
  sentiment_national = get_news_national()
  sentiment_company = [headline_sentiment(headline) for headline in sentiment_company]
  sentiment_national = [headline_sentiment(headline) for headline in sentiment_national]


  ### Calculate average company sentiment
  company_sentiment = np.mean([headline["compound"] for headline in sentiment_company])
  national_sentiment = np.mean([headline["compound"] for headline in sentiment_national])

  return {
      "company_sentiment": company_sentiment,
      "national_sentiment": national_sentiment
  }
