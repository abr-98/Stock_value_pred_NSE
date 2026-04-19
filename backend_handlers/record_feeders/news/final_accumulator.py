import pandas as pd
from .scrape_moneycontrol import scrape_moneycontrol_news
from .rss_scrapers import fetch_rss_news
from .google_news import fetch_google_news
from datetime import datetime
import yfinance as yf


# ---------------------------
# HELPERS
# ---------------------------
def normalize_news(news_list, source_name):
    normalized = []

    for n in news_list:
        normalized.append({
            "title": n.get("title"),
            "url": n.get("url") or n.get("link"),
            "source": n.get("source", source_name),
            "published": n.get("published") or n.get("providerPublishTime"),
            "scraped_at": n.get("scraped_at", datetime.now().isoformat())
        })

    return normalized


# ---------------------------
# YFINANCE NEWS
# ---------------------------
def fetch_yfinance_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news or []

    return [{
        "title": n.get("title"),
        "url": n.get("link"),
        "source": "Yahoo Finance",
        "published": n.get("providerPublishTime"),
        "scraped_at": datetime.now().isoformat()
    } for n in news]


# ---------------------------
# MAIN COMBINER
# ---------------------------
def build_news_dataframe(company_slug, keywords, ticker):
    
    # 1. Moneycontrol
    df_mc = scrape_moneycontrol_news(company_slug)
    
    # filter relevance
    df_mc = df_mc[df_mc["title"].str.lower().apply(
        lambda x: any(k in x for k in keywords)
    )]

    mc_news = df_mc.to_dict("records")


    # 2. RSS
    rss_news = fetch_rss_news(keywords)


    # 3. Google News
    gnews = []
    for kw in keywords:
        gnews.extend(fetch_google_news(kw))


    # 4. Yahoo Finance
    yf_news = fetch_yfinance_news(ticker)


    # ---------------------------
    # NORMALIZE
    # ---------------------------
    all_news = []
    all_news += normalize_news(mc_news, "Moneycontrol")
    all_news += normalize_news(rss_news, "RSS")
    all_news += normalize_news(gnews, "Google News")
    all_news += normalize_news(yf_news, "Yahoo Finance")


    # ---------------------------
    # CREATE DATAFRAME
    # ---------------------------
    df = pd.DataFrame(all_news)

    # drop nulls
    df = df.dropna(subset=["title", "url"])

    # ---------------------------
    # DEDUPLICATION
    # ---------------------------
    df = df.drop_duplicates(subset=["url"])
    
    df["company"] = company_slug
    
    df["date"] = pd.to_datetime(
    df["published"],
    format="mixed",     # handles multiple formats
    errors="coerce",    # avoids crashes
    utc=True            # standardize timezone
    )
    
    df["date"] = df["date"].fillna(pd.Timestamp.now(tz="UTC"))

    # Extract year, month, day
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    
    df["year"] = df["year"].astype("int32")
    df["month"] = df["month"].astype("int32")
    df["day"] = df["day"].astype("int32")

    # optional: sort by time
    df = df.sort_values(by="published", ascending=False, na_position="last")
    
    df_final = df[["company", "title", "url", "year", "month", "day"]]

    return df_final