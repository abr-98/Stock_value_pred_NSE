"""
Fundamental analysis router - handles fundamental report API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import FundamentalReportRequest, FundamentalReportResponse, ErrorResponse
from application.engines.fundamental_report_engine import FundamentalReportEngine
from apis.logging_config import setup_logging, log_service_io

router = APIRouter()
logger = setup_logging("service-fundamental-router")


@router.post(
    "/report",
    response_model=FundamentalReportResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Fundamental Report",
    description="Generates a comprehensive fundamental analysis report for a stock"
)
async def get_fundamental_report(request: FundamentalReportRequest, api_request: Request):
    """
    Get fundamental analysis report for a stock
    
    Args:
        request: FundamentalReportRequest containing the stock symbol
    
    Returns:
        FundamentalReportResponse with fundamental analysis report
    """
    try:
        log_service_io(logger, "fundamental.report.request", inputs={"symbol": request.symbol})
        logger.info(f"Starting fundamental report generation for symbol: {request.symbol}")
        
        # Initialize and run the fundamental report engine
        # Use pre-initialized agents if available (from app startup)
        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = FundamentalReportEngine(agents=agents)
        report = engine.run(request.symbol)
        log_service_io(
            logger,
            "fundamental.report.response",
            outputs={"symbol": request.symbol, "report_keys": list(report.keys()) if isinstance(report, dict) else []},
        )
        
        logger.info(f"Successfully generated fundamental report for symbol: {request.symbol}")
        
        return FundamentalReportResponse(
            status="success",
            symbol=request.symbol,
            report=report
        )
    
    except Exception as e:
        logger.error(f"Error generating fundamental report for {request.symbol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate fundamental report: {str(e)}"
        )


@router.get(
    "/report/{symbol}",
    response_model=FundamentalReportResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Fundamental Report (GET)",
    description="Generates a comprehensive fundamental analysis report using GET method"
)
async def get_fundamental_report_get(symbol: str, api_request: Request):
    """
    Get fundamental analysis report for a stock using GET method
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        FundamentalReportResponse with fundamental analysis report
    """
    request = FundamentalReportRequest(symbol=symbol)
    return await get_fundamental_report(request, api_request)
