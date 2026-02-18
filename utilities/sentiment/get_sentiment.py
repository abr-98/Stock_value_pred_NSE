from utilites.sentiment.get_news_company import get_news_company
from utilites.sentiment.get_news_national import get_news_national
from utilites.sentiment.fetch_sentiments import headline_sentiment
from utilites.sentiment.sentiment_pressure import sentiment_pressure
from utilites.sentiment.sentiment_shock import sentiment_shock
from utilites.sentiment.safe_mean import safe_mean
from utilites.sentiment.extract_extreme_sentiment import extract_extremes
from utilites.serialization_helper import convert_to_serializable
import numpy as np

def get_sentiment(ticker):

    sentiment_company_raw = get_news_company(ticker)
    sentiment_national_raw = get_news_national()

    sentiment_company = [headline_sentiment(h) for h in sentiment_company_raw]
    sentiment_national = [headline_sentiment(h) for h in sentiment_national_raw]

    company_compounds = [h["compound"] for h in sentiment_company]
    national_compounds = [h["compound"] for h in sentiment_national]

    company_extremes = extract_extremes(sentiment_company)
    national_extremes = extract_extremes(sentiment_national)

    company_sentiment = safe_mean(company_compounds)
    national_sentiment = safe_mean(national_compounds)

    result = {
        "company_sentiment": round(company_sentiment, 3),
        "national_sentiment": round(national_sentiment, 3),

        "company_positive_news": company_extremes["positive_count"],
        "company_negative_news": company_extremes["negative_count"],

        "company_sentiment_pressure": round(
            sentiment_pressure(company_extremes), 3
        ),

        "sentiment_shock": sentiment_shock(company_extremes)
    }
    
    # Convert all numpy/pandas types to Python native types
    return convert_to_serializable(result)

