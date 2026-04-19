import feedparser
from datetime import datetime

def fetch_google_news(keyword, limit=10):
    url = f"https://news.google.com/rss/search?q={keyword}+stock&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.get("title"),
            "url": entry.get("link"),
            "source": "Google News",
            "published": entry.get("published"),
            "scraped_at": datetime.now().isoformat()
        })

    return articles