"""
FastAPI application for Stock Predictor System
Main entry point for the API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
import os
import logging

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from apis.routers import (
    stock_router,
    portfolio_router,
    allocation_router,
    correlation_router,
    fundamental_router,
    memory_router,
    explain_router,
    qna_router,
    swot_router,
    user_router,
)
from user_handler.database_utilites.account.table_creators import create_user_tables
from environment import load_api_key
from application.helpers.initializers import SystemInitializer
from apis.logging_config import setup_logging, install_utility_call_tracer

logger = setup_logging("stock-predictor-api")
install_utility_call_tracer("service-utility-tracer-api")

# Initialize FastAPI app
app = FastAPI(
    title="Stock Predictor API",
    description="API for stock analysis, portfolio management, and market predictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

frontend_dir = os.path.join(project_root, "frontend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your security requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend assets from FastAPI when available.
if os.path.isdir(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")


@app.on_event("startup")
async def startup_event():
    """
    Initialize the system on startup
    - Load OpenAI API key from environment
    - Initialize vector database
    - Initialize all agents
    """
    logger.info("=" * 70)
    logger.info("Starting Stock Predictor API...")
    logger.info("=" * 70)
    
    try:
        # Load API key from OpenAI-Key.txt
        logger.info("Loading OpenAI API key...")
        load_api_key()
        logger.info("OpenAI API key loaded successfully")
        
        # Initialize system (agents, vector DB, etc.)
        logger.info("Initializing system components...")
        system_initializer = SystemInitializer()
        system_initializer.initialize_system()
        logger.info("System initialized successfully")

        logger.info("Ensuring user/account tables exist...")
        create_user_tables()
        logger.info("User/account tables verified")
        
        # Store initialized agents in app state for reuse
        app.state.system_initializer = system_initializer
        app.state.agents = system_initializer.get_agents()
        
        logger.info("=" * 70)
        logger.info("Stock Predictor API is ready!")
        logger.info("=" * 70)
        
    except FileNotFoundError:
        logger.exception("Could not find OpenAI-Key.txt in the project root")
        raise
    except Exception as e:
        logger.exception("Error during startup: %s", str(e))
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Stock Predictor API...")


# Include routers
app.include_router(stock_router.router, prefix="/api/v1/stock", tags=["Stock Analysis"])
app.include_router(portfolio_router.router, prefix="/api/v1/portfolio", tags=["Portfolio"])
app.include_router(allocation_router.router, prefix="/api/v1/allocation", tags=["Allocation"])
app.include_router(correlation_router.router, prefix="/api/v1/correlation", tags=["Correlation"])
app.include_router(fundamental_router.router, prefix="/api/v1/fundamental", tags=["Fundamental"])
app.include_router(memory_router.router, prefix="/api/v1/memory", tags=["Memory"])
app.include_router(explain_router.router, prefix="/api/v1/explain", tags=["Explain"])
app.include_router(qna_router.router, prefix="/api/v1/qna", tags=["QnA & Summarization"])
app.include_router(swot_router.router, prefix="/api/v1/swot", tags=["SWOT Analysis"])
app.include_router(user_router.router, prefix="/api/v1/users", tags=["User Accounts"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Stock Predictor API is running",
        "version": "1.0.0",
        "status": "healthy",
        "frontend": "/app" if os.path.isdir(frontend_dir) else None,
    }


@app.get("/app")
async def frontend_app():
    """Entry route for frontend app."""
    if not os.path.isdir(frontend_dir):
        raise HTTPException(status_code=404, detail="Frontend directory not found")
    return RedirectResponse(url="/frontend/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "stock-predictor-api"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled exception at path %s", getattr(request, "url", "unknown"))
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal error occurred",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
