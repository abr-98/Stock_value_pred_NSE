"""
Portfolio analysis router - handles portfolio-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import PortfolioAnalysisRequest, PortfolioAnalysisResponse, ErrorResponse
from application.engines.portfolio_data_engine import PortfolioDataEngine
from apis.logging_config import setup_logging, log_service_io

router = APIRouter()
logger = setup_logging("service-portfolio-router")


@router.post(
    "/analyze",
    response_model=PortfolioAnalysisResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Portfolio",
    description="Performs comprehensive portfolio analysis including performance metrics and diversification assessment"
)
async def analyze_portfolio(request: PortfolioAnalysisRequest, api_request: Request):
    """
    Analyze a portfolio and return analysis results
    
    Args:
        request: PortfolioAnalysisRequest containing portfolio data and value
    
    Returns:
        PortfolioAnalysisResponse with comprehensive portfolio analysis
    """
    try:
        log_service_io(
            logger,
            "portfolio.analyze.request",
            inputs={"holding_count": len(request.portfolio), "value": request.value},
        )
        logger.info(f"Starting portfolio analysis for value: {request.value}")
        
        # Initialize and run the portfolio data engine
        # Use pre-initialized agents if available (from app startup)
        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = PortfolioDataEngine(agents=agents)
        result = engine.run(request.portfolio, request.value)
        log_service_io(
            logger,
            "portfolio.analyze.response",
            outputs={"result_keys": list(result.keys()) if isinstance(result, dict) else []},
        )
        
        logger.info("Successfully completed portfolio analysis")
        
        return PortfolioAnalysisResponse(
            status="success",
            portfolio_analysis=result["portfolio_analysis"],
            diversification_analysis=result["diversification_analysis"],
            rationale=result["rationale"]
        )
    
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze portfolio: {str(e)}"
        )
