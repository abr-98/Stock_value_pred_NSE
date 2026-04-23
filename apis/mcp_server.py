"""
FastMCP server exposing Stock Predictor capabilities as MCP tools.
"""
from __future__ import annotations

import os
import sys
import threading
import importlib
import logging
from typing import Any, Dict, Optional

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from environment import load_api_key
from application.helpers.initializers import SystemInitializer
from application.engines.stock_data_engine import StockDataEngine
from application.engines.portfolio_data_engine import PortfolioDataEngine
from application.engines.allocation_data_engine import StockDataEngine as AllocationDataEngine
from application.engines.correlation_data_engine import CorrelationDataEngine
from application.engines.fundamental_report_engine import FundamentalReportEngine
from application.engines.memory_data_engine import MemoryDataEngine
from application.engines.explain_data_engine import ExplainDataEngine
from apis.logging_config import setup_logging

logger = setup_logging("stock-predictor-mcp")


class RuntimeContext:
    """Lazy, thread-safe runtime initializer shared by all MCP tools."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._initialized = False
        self._agents: Optional[Dict[str, Any]] = None

    def ensure_initialized(self) -> Dict[str, Any]:
        if self._initialized and self._agents is not None:
            return self._agents

        with self._lock:
            if self._initialized and self._agents is not None:
                return self._agents

            logger.info("Initializing MCP runtime context")
            load_api_key()
            initializer = SystemInitializer()
            initializer.initialize_system()
            self._agents = initializer.get_agents()
            self._initialized = True
            logger.info("MCP runtime context initialized")

        return self._agents


runtime = RuntimeContext()


def _create_mcp() -> Any:
    try:
        fastmcp_module = importlib.import_module("fastmcp")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency 'fastmcp'. Install it with: pip install fastmcp"
        ) from exc

    return fastmcp_module.FastMCP(name="stock-predictor-tools")


mcp = _create_mcp()


@mcp.tool(
    name="health_check",
    description="Check whether the Stock Predictor MCP server is healthy and initialized.",
)
def health_check() -> Dict[str, str]:
    runtime.ensure_initialized()
    logger.info("MCP health check successful")
    return {
        "status": "healthy",
        "service": "stock-predictor-mcp",
    }


@mcp.tool(
    name="analyze_stock",
    description="Perform comprehensive stock analysis (technical, fundamental, sentiment, regime, risk).",
)
def analyze_stock(symbol: str) -> Dict[str, Any]:
    logger.info("MCP analyze_stock started for symbol=%s", symbol)
    agents = runtime.ensure_initialized()
    engine = StockDataEngine()
    engine.agents = agents
    result = engine.run(symbol)
    logger.info("MCP analyze_stock completed for symbol=%s", symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "data": result,
    }


@mcp.tool(
    name="analyze_portfolio",
    description="Analyze a portfolio and return portfolio + diversification analysis.",
)
def analyze_portfolio(portfolio: Dict[str, Any], value: float) -> Dict[str, Any]:
    logger.info("MCP analyze_portfolio started with holdings=%d value=%s", len(portfolio), value)
    agents = runtime.ensure_initialized()
    engine = PortfolioDataEngine(agents=agents)
    result = engine.run(portfolio, value)
    logger.info("MCP analyze_portfolio completed")

    return {
        "status": "success",
        "portfolio_analysis": result["portfolio_analysis"],
        "diversification_analysis": result["diversification_analysis"],
        "rationale": result["rationale"],
    }


@mcp.tool(
    name="get_allocation",
    description="Generate allocation recommendations from current market conditions and optional portfolio.",
)
def get_allocation(
    portfolio: Optional[Dict[str, int]] = None,
    value: Optional[float] = None,
) -> Dict[str, Any]:
    logger.info(
        "MCP get_allocation started with holdings=%d value=%s",
        len(portfolio) if portfolio else 0,
        value,
    )
    agents = runtime.ensure_initialized()
    engine = AllocationDataEngine(agents=agents)
    result = engine.run(portfolio, value)
    logger.info("MCP get_allocation completed")

    return {
        "status": "success",
        "allocation_analysis": result["allocation_analysis"],
    }


@mcp.tool(
    name="analyze_correlation",
    description="Analyze stock correlation patterns for a symbol.",
)
def analyze_correlation(symbol: str) -> Dict[str, Any]:
    logger.info("MCP analyze_correlation started for symbol=%s", symbol)
    agents = runtime.ensure_initialized()
    engine = CorrelationDataEngine(agents=agents)
    correlation_report, rationale = engine.run(symbol)
    logger.info("MCP analyze_correlation completed for symbol=%s", symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "correlation_report": correlation_report,
        "rationale": rationale,
    }


@mcp.tool(
    name="get_fundamental_report",
    description="Generate a comprehensive fundamental report for a symbol.",
)
def get_fundamental_report(symbol: str) -> Dict[str, Any]:
    logger.info("MCP get_fundamental_report started for symbol=%s", symbol)
    agents = runtime.ensure_initialized()
    engine = FundamentalReportEngine(agents=agents)
    report = engine.run(symbol)
    logger.info("MCP get_fundamental_report completed for symbol=%s", symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "report": report,
    }


@mcp.tool(
    name="analyze_memory",
    description="Run memory-pattern analysis for a stock symbol.",
)
def analyze_memory(symbol: str) -> Dict[str, Any]:
    logger.info("MCP analyze_memory started for symbol=%s", symbol)
    agents = runtime.ensure_initialized()
    engine = MemoryDataEngine(agents=agents)
    report = engine.run(symbol)
    logger.info("MCP analyze_memory completed for symbol=%s", symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "report": report,
    }


@mcp.tool(
    name="analyze_explain",
    description="Run explainability analysis for a stock symbol.",
)
def analyze_explain(symbol: str) -> Dict[str, Any]:
    logger.info("MCP analyze_explain started for symbol=%s", symbol)
    agents = runtime.ensure_initialized()
    engine = ExplainDataEngine(agents=agents)
    report = engine.run(symbol)
    logger.info("MCP analyze_explain completed for symbol=%s", symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "report": report,
    }


@mcp.tool(
    name="query_transcripts",
    description=(
        "Answer a natural-language question using corporate annual-report PDFs and "
        "earnings-call transcripts for a given company. "
        "Builds a vector store from downloaded documents and returns the most relevant chunks."
    ),
)
def query_transcripts(
    company_slug: str,
    query: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    import os
    from utilities.QnA_summarization_Engine.transcripts_handler.fetch_and_answer_tool import (
        FetchAndAnswerTool,
    )

    logger.info("MCP query_transcripts started for company_slug=%s", company_slug)
    if workspace_root is None:
        workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    tool = FetchAndAnswerTool(company_slug=company_slug, workspace_root=workspace_root)
    tool.setup()
    raw_results = tool.answer_query(query)

    results = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in raw_results
    ]
    logger.info("MCP query_transcripts completed with %d chunks", len(results))

    return {
        "status": "success",
        "company_slug": company_slug,
        "query": query,
        "results": results,
    }


@mcp.tool(
    name="get_company_news",
    description="Fetch recent news articles (last 3 days) for a given company slug/ticker.",
)
def get_company_news(company_slug: str) -> Dict[str, Any]:
    from utilities.QnA_summarization_Engine.news.read_news import read_news_from_database

    logger.info("MCP get_company_news started for company_slug=%s", company_slug)
    df = read_news_from_database(company_slug)
    news_records = df.to_dict(orient="records") if df is not None and not df.empty else []
    logger.info("MCP get_company_news completed with %d records", len(news_records))

    return {
        "status": "success",
        "company_slug": company_slug,
        "news": news_records,
    }


@mcp.tool(
    name="swot_analysis",
    description=(
        "Perform absolute and peer-relative SWOT analysis for an NSE-listed stock ticker. "
        "Returns strengths, weaknesses, opportunities, and threats derived from fundamental metrics."
    ),
)
def swot_analysis(ticker: str) -> Dict[str, Any]:
    from utilities.swot_tool.swot_analysis_final import swot_analysis_final

    logger.info("MCP swot_analysis started for ticker=%s", ticker)
    result = swot_analysis_final(ticker)
    logger.info("MCP swot_analysis completed for ticker=%s", ticker)

    return {
        "status": "success",
        "ticker": ticker,
        "swot": result,
    }


if __name__ == "__main__":
    logger.info("Starting MCP server with stdio transport")
    mcp.run(transport="stdio")
