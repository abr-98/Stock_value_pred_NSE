"""
FastMCP server exposing Stock Predictor capabilities as MCP tools.
"""
from __future__ import annotations

import os
import sys
import threading
import importlib
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

            load_api_key()
            initializer = SystemInitializer()
            initializer.initialize_system()
            self._agents = initializer.get_agents()
            self._initialized = True

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
    return {
        "status": "healthy",
        "service": "stock-predictor-mcp",
    }


@mcp.tool(
    name="analyze_stock",
    description="Perform comprehensive stock analysis (technical, fundamental, sentiment, regime, risk).",
)
def analyze_stock(symbol: str) -> Dict[str, Any]:
    agents = runtime.ensure_initialized()
    engine = StockDataEngine()
    engine.agents = agents
    result = engine.run(symbol)

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
    agents = runtime.ensure_initialized()
    engine = PortfolioDataEngine(agents=agents)
    result = engine.run(portfolio, value)

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
    agents = runtime.ensure_initialized()
    engine = AllocationDataEngine(agents=agents)
    result = engine.run(portfolio, value)

    return {
        "status": "success",
        "allocation_analysis": result["allocation_analysis"],
    }


@mcp.tool(
    name="analyze_correlation",
    description="Analyze stock correlation patterns for a symbol.",
)
def analyze_correlation(symbol: str) -> Dict[str, Any]:
    agents = runtime.ensure_initialized()
    engine = CorrelationDataEngine(agents=agents)
    correlation_report, rationale = engine.run(symbol)

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
    agents = runtime.ensure_initialized()
    engine = FundamentalReportEngine(agents=agents)
    report = engine.run(symbol)

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
    agents = runtime.ensure_initialized()
    engine = MemoryDataEngine(agents=agents)
    report = engine.run(symbol)

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
    agents = runtime.ensure_initialized()
    engine = ExplainDataEngine(agents=agents)
    report = engine.run(symbol)

    return {
        "status": "success",
        "symbol": symbol,
        "report": report,
    }


if __name__ == "__main__":
    # Use stdio transport so MCP clients (VS Code, Claude Desktop, etc.) can connect.
    mcp.run(transport="stdio")
