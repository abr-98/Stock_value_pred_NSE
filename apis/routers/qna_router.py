"""
QnA Summarization Engine router - handles transcript Q&A and news endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Any
from apis.models.schemas import (
    QnAQueryRequest,
    QnAQueryResponse,
    NewsRequest,
    NewsResponse,
    ErrorResponse,
)
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/query",
    response_model=QnAQueryResponse,
    responses={500: {"model": ErrorResponse, "description": "Internal Server Error"}},
    summary="Answer question from corporate transcripts",
    description=(
        "Builds (or reuses) a vector store from downloaded annual-report PDFs / "
        "earnings-call transcripts for the given company and returns the most "
        "relevant document chunks that answer the question."
    ),
)
async def query_transcripts(request: QnAQueryRequest):
    try:
        logger.info(f"QnA query for '{request.company_slug}': {request.query}")

        from utilities.QnA_summarization_Engine.transcripts_handler.fetch_and_answer_tool import (
            FetchAndAnswerTool,
        )

        tool = FetchAndAnswerTool(company_slug=request.company_slug)
        tool.setup()
        raw_results = tool.answer_query(request.query)

        # Convert LangChain Document objects to serialisable dicts
        results = []
        for doc in raw_results:
            results.append(
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata,
                }
            )

        logger.info(
            f"QnA query completed for '{request.company_slug}', {len(results)} chunks returned"
        )
        return QnAQueryResponse(
            status="success",
            company_slug=request.company_slug,
            query=request.query,
            results=results,
        )

    except Exception as e:
        logger.error(f"QnA query error for '{request.company_slug}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"QnA query failed: {e}")


@router.post(
    "/news",
    response_model=NewsResponse,
    responses={500: {"model": ErrorResponse, "description": "Internal Server Error"}},
    summary="Fetch recent news for a company",
    description="Returns news articles from the last 3 days for the given company slug.",
)
async def get_news(request: NewsRequest):
    try:
        logger.info(f"Fetching news for '{request.company_slug}'")

        from utilities.QnA_summarization_Engine.news.read_news import read_news_from_database

        df = read_news_from_database(request.company_slug)
        news_records: list[dict[str, Any]] = (
            [{str(k): v for k, v in row.items()} for row in df.to_dict(orient="records")]
            if df is not None and not df.empty
            else []
        )

        logger.info(f"News fetch completed for '{request.company_slug}', {len(news_records)} records")
        return NewsResponse(
            status="success",
            company_slug=request.company_slug,
            news=news_records,
        )

    except Exception as e:
        logger.error(f"News fetch error for '{request.company_slug}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"News fetch failed: {e}")


@router.get(
    "/news/{company_slug}",
    response_model=NewsResponse,
    responses={500: {"model": ErrorResponse, "description": "Internal Server Error"}},
    summary="Fetch recent news for a company (GET)",
    description="Returns news articles from the last 3 days for the given company slug.",
)
async def get_news_by_slug(company_slug: str):
    return await get_news(NewsRequest(company_slug=company_slug))
