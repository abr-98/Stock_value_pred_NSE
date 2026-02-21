"""
Explain analysis router - handles explain analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import ExplainAnalysisRequest, ExplainAnalysisResponse, ErrorResponse
from application.engines.explain_data_engine import ExplainDataEngine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/analyze",
    response_model=ExplainAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Explain",
    description="Runs explainability analysis for a given stock symbol"
)
async def analyze_explain(request: ExplainAnalysisRequest, api_request: Request):
    """
    Analyze explainability signals for a stock

    Args:
        request: ExplainAnalysisRequest containing the stock symbol

    Returns:
        ExplainAnalysisResponse with explain analysis report
    """
    try:
        logger.info(f"Starting explain analysis for symbol: {request.symbol}")

        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = ExplainDataEngine(agents=agents)
        report = engine.run(request.symbol)

        logger.info(f"Successfully completed explain analysis for symbol: {request.symbol}")

        return ExplainAnalysisResponse(
            status="success",
            symbol=request.symbol,
            report=report
        )

    except Exception as e:
        logger.error(f"Error analyzing explain for {request.symbol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze explain: {str(e)}"
        )


@router.get(
    "/analyze/{symbol}",
    response_model=ExplainAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Explain (GET)",
    description="Runs explainability analysis using GET method"
)
async def analyze_explain_get(symbol: str, api_request: Request):
    """
    Analyze explainability signals for a stock using GET method

    Args:
        symbol: Stock ticker symbol

    Returns:
        ExplainAnalysisResponse with explain analysis report
    """
    request = ExplainAnalysisRequest(symbol=symbol)
    return await analyze_explain(request, api_request)
