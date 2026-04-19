import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_moneycontrol_news(company_slug, pages=3):
    base_url = f"https://www.moneycontrol.com/news/tags/{company_slug}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_news = []

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}page-{page}/"

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        articles = soup.select("li.clearfix")

        print(f"Scraping page {page} - found {len(articles)} articles")

        for article in articles:
            try:
                # ✅ New selector
                title_tag = article.select_one("h2.related_des")

                if not title_tag:
                    continue  # skip login/ads blocks

                title = title_tag.text.strip()

                # ✅ URL now from parent <a>
                link_tag = article.select_one("a")
                url = link_tag.get("href") if link_tag else ""

                all_news.append({
                    "title": title,
                    "url": url
                })

            except Exception as e:
                print("ERROR:", e)

    print("Total collected:", len(all_news))

    return pd.DataFrame(all_news)