"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


# Request Models
class StockAnalysisRequest(BaseModel):
    """Request model for stock analysis"""
    symbol: str = Field(..., description="Stock symbol to analyze", example="AAPL")


class PortfolioAnalysisRequest(BaseModel):
    """Request model for portfolio analysis"""
    portfolio: Dict[str, Any] = Field(..., description="Portfolio holdings data")
    value: float = Field(..., description="Total portfolio value", example=100000.0)


class AllocationRequest(BaseModel):
    """Request model for allocation analysis"""
    portfolio: Optional[Dict[str, int]] = Field(default=None, description="Optional portfolio holdings (stock symbol: quantity)")
    value: Optional[float] = Field(default=None, description="Optional total portfolio value", example=100000.0)


class CorrelationAnalysisRequest(BaseModel):
    """Request model for correlation analysis"""
    symbol: str = Field(..., description="Stock symbol to analyze", example="AAPL")


class FundamentalReportRequest(BaseModel):
    """Request model for fundamental report"""
    symbol: str = Field(..., description="Stock symbol to analyze", example="AAPL")


class MemoryAnalysisRequest(BaseModel):
    """Request model for memory analysis"""
    symbol: str = Field(..., description="Stock symbol to analyze", example="AAPL")


class ExplainAnalysisRequest(BaseModel):
    """Request model for explain analysis"""
    symbol: str = Field(..., description="Stock symbol to analyze", example="AAPL")


# Response Models
class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis"""
    status: str = Field(default="success", description="Response status")
    symbol: str = Field(..., description="Analyzed stock symbol")
    data: Dict[str, Any] = Field(..., description="Aggregated stock signals and analysis")


class PortfolioAnalysisResponse(BaseModel):
    """Response model for portfolio analysis"""
    status: str = Field(default="success", description="Response status")
    portfolio_analysis: Dict[str, Any] = Field(..., description="Portfolio analysis results")
    diversification_analysis: Dict[str, Any] = Field(..., description="Diversification analysis results")
    rationale: str = Field(..., description="Analysis rationale")


class AllocationResponse(BaseModel):
    """Response model for allocation analysis"""
    status: str = Field(default="success", description="Response status")
    allocation_analysis: Dict[str, Any] = Field(..., description="Asset allocation recommendations")


class CorrelationAnalysisResponse(BaseModel):
    """Response model for correlation analysis"""
    status: str = Field(default="success", description="Response status")
    symbol: str = Field(..., description="Analyzed stock symbol")
    correlation_report: Dict[str, Any] = Field(..., description="Correlation analysis report")
    rationale: str = Field(..., description="Analysis rationale")


class FundamentalReportResponse(BaseModel):
    """Response model for fundamental report"""
    status: str = Field(default="success", description="Response status")
    symbol: str = Field(..., description="Analyzed stock symbol")
    report: Dict[str, Any] = Field(..., description="Fundamental analysis report")


class MemoryAnalysisResponse(BaseModel):
    """Response model for memory analysis"""
    status: str = Field(default="success", description="Response status")
    symbol: str = Field(..., description="Analyzed stock symbol")
    report: Dict[str, Any] = Field(..., description="Memory analysis report")


class ExplainAnalysisResponse(BaseModel):
    """Response model for explain analysis"""
    status: str = Field(default="success", description="Response status")
    symbol: str = Field(..., description="Analyzed stock symbol")
    report: Dict[str, Any] = Field(..., description="Explain analysis report")


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field(default="error", description="Response status")
    message: str = Field(..., description="Error message")


# QnA Summarization Engine models
class QnAQueryRequest(BaseModel):
    """Request model for transcript Q&A query"""
    company_slug: str = Field(..., description="Company slug/ticker identifier", example="TCS.NS")
    query: str = Field(..., description="Natural language question about the company's transcripts", example="What was the revenue growth in Q3?")
    workspace_root: Optional[str] = Field(default=None, description="Optional path to workspace root; defaults to project root")


class QnAQueryResponse(BaseModel):
    """Response model for transcript Q&A query"""
    status: str = Field(default="success", description="Response status")
    company_slug: str = Field(..., description="Company slug queried")
    query: str = Field(..., description="The question asked")
    results: List[Dict[str, Any]] = Field(..., description="Relevant document chunks returned by the vector store")


class NewsRequest(BaseModel):
    """Request model for fetching recent news"""
    company_slug: str = Field(..., description="Company slug/ticker identifier", example="TCS.NS")


class NewsResponse(BaseModel):
    """Response model for recent news"""
    status: str = Field(default="success", description="Response status")
    company_slug: str = Field(..., description="Company slug queried")
    news: List[Dict[str, Any]] = Field(..., description="Recent news articles from the last 3 days")


# SWOT Analysis models
class SwotAnalysisRequest(BaseModel):
    """Request model for SWOT analysis"""
    ticker: str = Field(..., description="Stock ticker symbol (NSE format)", example="TCS.NS")


class SwotAnalysisResponse(BaseModel):
    """Response model for SWOT analysis"""
    status: str = Field(default="success", description="Response status")
    ticker: str = Field(..., description="Analysed stock ticker")
    swot: Dict[str, Any] = Field(..., description="SWOT analysis result with strengths, weaknesses, opportunities, and threats")
    detail: Optional[str] = Field(None, description="Detailed error information")
