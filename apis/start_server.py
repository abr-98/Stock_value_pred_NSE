"""
Quick start script for the FastAPI Stock Predictor API
"""
import sys
import os

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apis.logging_config import setup_logging

if __name__ == "__main__":
    import uvicorn
    from apis.config import settings
    logger = setup_logging("stock-predictor-api-launcher")
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║   Stock Predictor API Server                          ║
    ║   Version: {settings.API_VERSION}                                     ║
    ╚═══════════════════════════════════════════════════════╝
    
    Starting server...
    - Host: {settings.HOST}
    - Port: {settings.PORT}
    - Docs: http://{settings.HOST if settings.HOST != '0.0.0.0' else 'localhost'}:{settings.PORT}/docs
    - ReDoc: http://{settings.HOST if settings.HOST != '0.0.0.0' else 'localhost'}:{settings.PORT}/redoc
    
    Press CTRL+C to stop the server
    """)
    logger.info("Launching FastAPI server on %s:%s", settings.HOST, settings.PORT)
    
    uvicorn.run(
        "apis.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
