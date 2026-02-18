"""
Models package initialization
"""
from apis.models.schemas import (
    StockAnalysisRequest,
    StockAnalysisResponse,
    PortfolioAnalysisRequest,
    PortfolioAnalysisResponse,
    AllocationRequest,
    AllocationResponse,
    CorrelationAnalysisRequest,
    CorrelationAnalysisResponse,
    FundamentalReportRequest,
    FundamentalReportResponse,
    ErrorResponse
)

__all__ = [
    "StockAnalysisRequest",
    "StockAnalysisResponse",
    "PortfolioAnalysisRequest",
    "PortfolioAnalysisResponse",
    "AllocationRequest",
    "AllocationResponse",
    "CorrelationAnalysisRequest",
    "CorrelationAnalysisResponse",
    "FundamentalReportRequest",
    "FundamentalReportResponse",
    "ErrorResponse"
]
