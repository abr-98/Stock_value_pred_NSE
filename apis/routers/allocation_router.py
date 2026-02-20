"""
Allocation router - handles asset allocation API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import AllocationRequest, AllocationResponse, ErrorResponse
from application.engines.allocation_data_engine import StockDataEngine  # Note: This should be renamed to AllocationDataEngine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/analyze",
    response_model=AllocationResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Allocation Recommendations",
    description="Analyzes market conditions and provides asset allocation recommendations"
)
async def get_allocation(request: AllocationRequest, api_request: Request):
    """
    Get allocation recommendations based on market analysis
    
    Args:
        request: AllocationRequest with optional portfolio data and value
                 If portfolio is provided, it will be used for diversification analysis
                 If portfolio is None/empty, fresh allocation recommendations will be provided
    
    Returns:
        AllocationResponse with allocation recommendations
    """
    try:
        portfolio_info = f"with portfolio ({len(request.portfolio)} holdings)" if request.portfolio else "without existing portfolio"
        logger.info(f"Starting allocation analysis {portfolio_info}")
        
        # Initialize and run the allocation engine
        # Use pre-initialized agents if available (from app startup)
        agents = api_request.app.state.agents if hasattr(api_request.app.state, 'agents') else None
        engine = StockDataEngine(agents=agents)  # Note: This class should be renamed to AllocationDataEngine
        result = engine.run(request.portfolio, request.value)
        
        logger.info("Successfully completed allocation analysis")
        
        return AllocationResponse(
            status="success",
            allocation_analysis=result["allocation_analysis"]
        )
    
    except Exception as e:
        logger.error(f"Error in allocation analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze allocation: {str(e)}"
        )
