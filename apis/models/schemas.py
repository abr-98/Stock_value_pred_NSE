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
    force_refresh: bool = Field(
        default=False,
        description="If true, redownload/rebuild the company transcript index before answering.",
    )


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


# User account, chat thread, token tracking, watchlist, and portfolio models
class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    plan_type: Optional[str] = Field(default="free", description="Plan type")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserProfileResponse(BaseModel):
    id: int
    email: str
    plan_type: str
    token_usage: int
    created_at: Any


class UserAuthResponse(BaseModel):
    status: str = "success"
    access_token: str
    token_type: str = "bearer"
    user: UserProfileResponse


class ThreadCreateRequest(BaseModel):
    title: Optional[str] = Field(default="New Chat", description="Thread title")


class ThreadResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: Any


class MessageCreateRequest(BaseModel):
    role: str = Field(..., description="user|assistant|system")
    content: str = Field(..., description="Message content")
    model: Optional[str] = Field(default="gpt-4o", description="LLM model name")
    input_tokens: Optional[int] = Field(default=None, description="Optional override for input tokens")
    output_tokens: Optional[int] = Field(default=None, description="Optional override for output tokens")


class MessageResponse(BaseModel):
    id: int
    thread_id: int
    role: str
    content: str
    token_count: int
    model: str
    created_at: Any


class TokenUsageRecordResponse(BaseModel):
    id: int
    user_id: int
    thread_id: Optional[int]
    input_tokens: int
    output_tokens: int
    total_tokens: int
    model: str
    cost: float
    timestamp: Any


class MessageCreateResponse(BaseModel):
    status: str = "success"
    message: MessageResponse
    usage: TokenUsageRecordResponse


class TokenUsageAggregateResponse(BaseModel):
    user_id: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    total_cost: float


class WatchlistCreateRequest(BaseModel):
    ticker: str = Field(..., description="Ticker symbol, e.g., INFY.NS")


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    ticker: str
    added_at: Any


class PortfolioCreateRequest(BaseModel):
    ticker: str = Field(..., description="Ticker symbol, e.g., INFY.NS")
    quantity: float = Field(..., gt=0, description="Position quantity")
    avg_buy_price: float = Field(..., gt=0, description="Average buy price")


class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    ticker: str
    quantity: float
    avg_buy_price: float
    created_at: Any
