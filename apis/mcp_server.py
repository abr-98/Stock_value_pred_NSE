"""
FastMCP server exposing Stock Predictor capabilities as MCP tools.
"""
from __future__ import annotations

import os
import sys
import threading
from typing import Any, Dict, Optional
from fastmcp import FastMCP

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

DEFAULT_MCP_PROFILE = "all"
ACTIVE_MCP_PROFILE = os.environ.get("MCP_AGENT_PROFILE", DEFAULT_MCP_PROFILE)


def _create_mcp() -> Any:
    return FastMCP(name="stock-predictor-tools")


def health_check() -> Dict[str, str]:
    runtime.ensure_initialized()
    logger.info("MCP health check successful")
    return {
        "status": "healthy",
        "service": "stock-predictor-mcp",
    }


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


TOOL_SPECS = {
    "health_check": {
        "description": "Check whether the Stock Predictor MCP server is healthy and initialized.",
        "handler": health_check,
    },
    "analyze_stock": {
        "description": "Perform comprehensive stock analysis (technical, fundamental, sentiment, regime, risk).",
        "handler": analyze_stock,
    },
    "analyze_portfolio": {
        "description": "Analyze a portfolio and return portfolio + diversification analysis.",
        "handler": analyze_portfolio,
    },
    "get_allocation": {
        "description": "Generate allocation recommendations from current market conditions and optional portfolio.",
        "handler": get_allocation,
    },
    "analyze_correlation": {
        "description": "Analyze stock correlation patterns for a symbol.",
        "handler": analyze_correlation,
    },
    "get_fundamental_report": {
        "description": "Generate a comprehensive fundamental report for a symbol.",
        "handler": get_fundamental_report,
    },
    "analyze_memory": {
        "description": "Run memory-pattern analysis for a stock symbol.",
        "handler": analyze_memory,
    },
    "analyze_explain": {
        "description": "Run explainability analysis for a stock symbol.",
        "handler": analyze_explain,
    },
    "query_transcripts": {
        "description": (
            "Answer a natural-language question using corporate annual-report PDFs and "
            "earnings-call transcripts for a given company. Builds a vector store from "
            "downloaded documents and returns the most relevant chunks."
        ),
        "handler": query_transcripts,
    },
    "get_company_news": {
        "description": "Fetch recent news articles (last 3 days) for a given company slug/ticker.",
        "handler": get_company_news,
    },
    "swot_analysis": {
        "description": (
            "Perform absolute and peer-relative SWOT analysis for an NSE-listed stock ticker. "
            "Returns strengths, weaknesses, opportunities, and threats derived from fundamental metrics."
        ),
        "handler": swot_analysis,
    },
}


PROFILE_TOOLS = {
    "all": list(TOOL_SPECS.keys()),
    "stock_aggregator": ["health_check", "analyze_stock"],
    "allocation_agent": ["health_check", "get_allocation"],
    "portfolio_agent": ["health_check", "analyze_portfolio"],
    "portfolio_analysis_agent": ["health_check", "analyze_portfolio"],
    "diversification_agent": ["health_check", "analyze_portfolio"],
    "correlation_agent": ["health_check", "analyze_correlation"],
    "fundamental_documents_agent": [
        "health_check",
        "get_fundamental_report",
        "query_transcripts",
        "get_company_news",
        "swot_analysis",
    ],
    "memory_agent": ["health_check", "analyze_memory"],
    "explain_agent": ["health_check", "analyze_explain"],
    "qna_agent": ["health_check", "query_transcripts", "get_company_news"],
    "swot_agent": ["health_check", "swot_analysis"],
}


def get_available_profiles() -> list[str]:
    return sorted(PROFILE_TOOLS.keys())


def create_mcp_server(profile: str = DEFAULT_MCP_PROFILE) -> Any:
    if profile not in PROFILE_TOOLS:
        raise ValueError(
            f"Unknown MCP profile '{profile}'. Available profiles: {', '.join(get_available_profiles())}"
        )

    server = _create_mcp()
    server.name = f"stock-predictor-tools-{profile}"

    for tool_name in PROFILE_TOOLS[profile]:
        spec = TOOL_SPECS[tool_name]
        server.tool(name=tool_name, description=spec["description"])(spec["handler"])

    logger.info("Created MCP server for profile=%s with tools=%s", profile, PROFILE_TOOLS[profile])
    return server


mcp = create_mcp_server(ACTIVE_MCP_PROFILE)


if __name__ == "__main__":
    logger.info("Starting MCP server with stdio transport for profile=%s", ACTIVE_MCP_PROFILE)
    mcp.run(transport="stdio")
