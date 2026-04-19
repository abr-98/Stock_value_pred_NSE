from .news.final_accumulator import build_news_dataframe
from ..database_utilities.write_database import insert_dataframe

def feed_news(company_slug, keywords, ticker):
    
    # 1. Fetch news
    news_df = build_news_dataframe(company_slug, keywords, ticker)
    
    print(news_df.head())
 
    # 3. Insert into database
    insert_dataframe(news_df, "news")