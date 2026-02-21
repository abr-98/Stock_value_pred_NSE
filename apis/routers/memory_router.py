"""
Memory analysis router - handles memory analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import MemoryAnalysisRequest, MemoryAnalysisResponse, ErrorResponse
from application.engines.memory_data_engine import MemoryDataEngine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/analyze",
    response_model=MemoryAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Memory",
    description="Runs memory-pattern analysis for a given stock symbol"
)
async def analyze_memory(request: MemoryAnalysisRequest, api_request: Request):
    """
    Analyze memory patterns for a stock

    Args:
        request: MemoryAnalysisRequest containing the stock symbol

    Returns:
        MemoryAnalysisResponse with memory analysis report
    """
    try:
        logger.info(f"Starting memory analysis for symbol: {request.symbol}")

        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = MemoryDataEngine(agents=agents)
        report = engine.run(request.symbol)

        logger.info(f"Successfully completed memory analysis for symbol: {request.symbol}")

        return MemoryAnalysisResponse(
            status="success",
            symbol=request.symbol,
            report=report
        )

    except Exception as e:
        logger.error(f"Error analyzing memory for {request.symbol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze memory: {str(e)}"
        )


@router.get(
    "/analyze/{symbol}",
    response_model=MemoryAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Memory (GET)",
    description="Runs memory-pattern analysis using GET method"
)
async def analyze_memory_get(symbol: str, api_request: Request):
    """
    Analyze memory patterns for a stock using GET method

    Args:
        symbol: Stock ticker symbol

    Returns:
        MemoryAnalysisResponse with memory analysis report
    """
    request = MemoryAnalysisRequest(symbol=symbol)
    return await analyze_memory(request, api_request)
