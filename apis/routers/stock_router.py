"""
Stock analysis router - handles stock-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import StockAnalysisRequest, StockAnalysisResponse, ErrorResponse
from application.engines.stock_data_engine import StockDataEngine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/analyze",
    response_model=StockAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Stock",
    description="Performs comprehensive stock analysis including technical, fundamental, sentiment, regime, and risk analysis"
)
async def analyze_stock(request: StockAnalysisRequest, api_request: Request):
    """
    Analyze a stock symbol and return aggregated signals
    
    Args:
        request: StockAnalysisRequest containing the stock symbol
    
    Returns:
        StockAnalysisResponse with comprehensive analysis data
    """
    try:
        logger.info(f"Starting stock analysis for symbol: {request.symbol}")
        
        # Initialize and run the stock data engine
        # Use pre-initialized agents if available (from app startup)
        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = StockDataEngine()
        if agents:
            engine.agents = agents
        result = engine.run(request.symbol)
        
        logger.info(f"Successfully completed stock analysis for symbol: {request.symbol}")
        
        return StockAnalysisResponse(
            status="success",
            symbol=request.symbol,
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error analyzing stock {request.symbol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze stock: {str(e)}"
        )


@router.get(
    "/analyze/{symbol}",
    response_model=StockAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Stock (GET)",
    description="Performs comprehensive stock analysis using GET method"
)
async def analyze_stock_get(symbol: str, api_request: Request):
    """
    Analyze a stock symbol using GET method
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        StockAnalysisResponse with comprehensive analysis data
    """
    request = StockAnalysisRequest(symbol=symbol)
    return await analyze_stock(request, api_request)
