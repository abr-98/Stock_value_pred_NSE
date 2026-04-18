import re
import feedparser
from datetime import datetime


RSS_SOURCES = {
    "Moneycontrol": "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "Economic Times": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "LiveMint": "https://www.livemint.com/rss/markets",
    "Business Standard": "https://www.business-standard.com/rss/markets-106.rss",
}

HEADERS = {"User-Agent": "Mozilla/5.0"}


# --- HELPERS ---
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_relevant(text, keywords):
    text = text.lower()
    return any(k.lower() in text for k in keywords)


# --- FETCH RSS ---
def fetch_rss_news(keywords, limit=20):
    articles = []

    for source, url in RSS_SOURCES.items():
        feed = feedparser.parse(url)
        print(f"Fetched {len(feed.entries)} entries from {source}")

        for entry in feed.entries[:limit]:
            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", ""))

            if not is_relevant(title + " " + summary, keywords):
                continue

            articles.append({
                "title": title,
                "summary": summary,
                "url": entry.get("link"),
                "source": source,
                "published": entry.get("published"),
                "scraped_at": datetime.now().isoformat()
            })

    return articles
