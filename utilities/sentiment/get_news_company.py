from utilities.datafeeds.yfinance_config import yf

def get_news_company(ticker):
  ticker = yf.Ticker(ticker)
  news = [news["content"]["summary"] for news in ticker.news]
  return news
