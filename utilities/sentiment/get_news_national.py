import feedparser
from utilites.sentiment.urls import RSS_FEEDS

def get_news_national():
  for url in RSS_FEEDS.values():
    feed = feedparser.parse(url)
    #print(feed)
    news = []

    for entry in feed.entries:
        news.append(entry.title
        )
    return news