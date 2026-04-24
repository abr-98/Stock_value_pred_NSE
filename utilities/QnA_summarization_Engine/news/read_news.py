from backend_handlers.database_utilities.execute_query import execute_query_to_dataframe
from apis.logging_config import setup_logging, log_service_io


logger = setup_logging("service-utility-qna-news")

def read_news_from_database(company_slug):
    log_service_io(logger, "utility.qna.news.request", inputs={"company_slug": company_slug})
    from datetime import datetime, timedelta

    date_str = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    query = f"""
    SELECT *
    FROM news_2
    WHERE company = '{company_slug}'
    AND MAKE_DATE(year, month, day) >= '{date_str}'
    """

    df = execute_query_to_dataframe(query)
    log_service_io(
        logger,
        "utility.qna.news.response",
        outputs={"company_slug": company_slug, "row_count": 0 if df is None else len(df)},
    )
    return df