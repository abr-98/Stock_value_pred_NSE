"""
SWOT Analysis router - exposes SWOT analysis endpoints
"""
from fastapi import APIRouter, HTTPException
from apis.models.schemas import SwotAnalysisRequest, SwotAnalysisResponse, ErrorResponse
from apis.logging_config import setup_logging, log_service_io

router = APIRouter()
logger = setup_logging("service-swot-router")


@router.post(
    "/analyze",
    response_model=SwotAnalysisResponse,
    responses={500: {"model": ErrorResponse, "description": "Internal Server Error"}},
    summary="SWOT Analysis",
    description=(
        "Performs both absolute and peer-relative SWOT analysis for the given NSE ticker. "
        "Returns a merged SWOT dict with Strengths, Weaknesses, Opportunities, and Threats."
    ),
)
async def analyze_swot(request: SwotAnalysisRequest):
    try:
        log_service_io(logger, "swot.analyze.request", inputs={"ticker": request.ticker})
        logger.info(f"Starting SWOT analysis for ticker: {request.ticker}")

        from utilities.swot_tool.swot_analysis_final import swot_analysis_final

        result = swot_analysis_final(request.ticker)
        log_service_io(
            logger,
            "swot.analyze.response",
            outputs={"ticker": request.ticker, "swot_keys": list(result.keys()) if isinstance(result, dict) else []},
        )

        logger.info(f"SWOT analysis completed for ticker: {request.ticker}")
        return SwotAnalysisResponse(
            status="success",
            ticker=request.ticker,
            swot=result,
        ) # type: ignore

    except Exception as e:
        logger.error(f"SWOT analysis error for '{request.ticker}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"SWOT analysis failed: {e}")


@router.get(
    "/analyze/{ticker}",
    response_model=SwotAnalysisResponse,
    responses={500: {"model": ErrorResponse, "description": "Internal Server Error"}},
    summary="SWOT Analysis (GET)",
    description="Performs SWOT analysis for the given NSE ticker (GET convenience endpoint).",
)
async def analyze_swot_get(ticker: str):
    return await analyze_swot(SwotAnalysisRequest(ticker=ticker))
