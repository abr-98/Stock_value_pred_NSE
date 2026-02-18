"""
Correlation analysis router - handles correlation analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import CorrelationAnalysisRequest, CorrelationAnalysisResponse, ErrorResponse
from application.engines.correlation_data_engine import CorrelationDataEngine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/analyze",
    response_model=CorrelationAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Stock Correlations",
    description="Analyzes correlation patterns for a given stock symbol"
)
async def analyze_correlation(request: CorrelationAnalysisRequest, api_request: Request):
    """
    Analyze correlation patterns for a stock
    
    Args:
        request: CorrelationAnalysisRequest containing the stock symbol
    
    Returns:
        CorrelationAnalysisResponse with correlation analysis
    """
    try:
        logger.info(f"Starting correlation analysis for symbol: {request.symbol}")
        
        # Initialize and run the correlation engine
        # Use pre-initialized agents if available (from app startup)
        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = CorrelationDataEngine(agents=agents)
        correlation_report, rationale = engine.run(request.symbol)
        
        logger.info(f"Successfully completed correlation analysis for symbol: {request.symbol}")
        
        return CorrelationAnalysisResponse(
            status="success",
            symbol=request.symbol,
            correlation_report=correlation_report,
            rationale=rationale
        )
    
    except Exception as e:
        logger.error(f"Error analyzing correlation for {request.symbol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze correlation: {str(e)}"
        )


@router.get(
    "/analyze/{symbol}",
    response_model=CorrelationAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Stock Correlations (GET)",
    description="Analyzes correlation patterns using GET method"
)
async def analyze_correlation_get(symbol: str, api_request: Request):
    """
    Analyze correlation patterns for a stock using GET method
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        CorrelationAnalysisResponse with correlation analysis
    """
    request = CorrelationAnalysisRequest(symbol=symbol)
    return await analyze_correlation(request, api_request)
