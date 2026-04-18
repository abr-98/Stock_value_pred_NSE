# FastAPI Stock Predictor API

## Overview
This FastAPI application provides REST endpoints for the Stock Predictor system, enabling access to various analysis engines including stock analysis, portfolio management, allocation recommendations, correlation analysis, and fundamental reports.

## System Initialization

The API automatically initializes the system on startup:

1. **Loads OpenAI API Key** from `OpenAI-Key.txt` in the project root
2. **Initializes Vector Database** for fundamental document storage
3. **Pre-initializes all agents** to improve performance:
   - Technical Analysis Agent
   - Sentiment Analysis Agent
   - Fundamental Analysis Agent
   - Risk Analysis Agent
   - Regime Stock Agent
   - Allocation Agent
   - Portfolio Analysis Agent
   - Diversification Agent
   - Correlation Agent
   - Fundamental Documents Agent

These pre-initialized agents are reused across all API requests, significantly improving response times.

## Features

- **Stock Analysis**: Comprehensive stock analysis including technical, fundamental, sentiment, regime, and risk analysis
- **Portfolio Analysis**: Portfolio performance metrics and diversification assessment  
- **Allocation Recommendations**: Market-based asset allocation suggestions
- **Correlation Analysis**: Stock correlation pattern analysis
- **Fundamental Reports**: Detailed fundamental analysis reports
- **Optimized Performance**: Agents initialized once on startup, reused across requests

Additional pre-initialized agents now exposed via API:
- Memory Agent
- Explain Agent

## Installation

1. Ensure `OpenAI-Key.txt` exists in the project root with your OpenAI API key

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

The requirements already include:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-multipart>=0.0.6
```

## Running the API

### Development Mode
```bash
cd apis
python main.py
```

Or using uvicorn directly:
```bash
uvicorn apis.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn apis.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Running As MCP Tools (FastMCP)

This project now includes an MCP server that exposes the same analysis capabilities as tools.

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MCP server (stdio transport):
```bash
python apis/start_mcp_server.py
```

You can also run directly:
```bash
python apis/mcp_server.py
```

### Available MCP Tools

- `health_check`
- `analyze_stock(symbol)`
- `analyze_portfolio(portfolio, value)`
- `get_allocation(portfolio=None, value=None)`
- `analyze_correlation(symbol)`
- `get_fundamental_report(symbol)`
- `analyze_memory(symbol)`
- `analyze_explain(symbol)`

### Example MCP Client Config (stdio)

```json
{
  "mcpServers": {
    "stock-predictor": {
      "command": "python",
      "args": ["apis/start_mcp_server.py"],
      "cwd": "D:/personal/Stock_value_pred_NSE"
    }
  }
}
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Stock Analysis
- `POST /api/v1/stock/analyze` - Analyze a stock (POST with JSON body)
- `GET /api/v1/stock/analyze/{symbol}` - Analyze a stock (GET method)

**Example Request (POST)**:
```json
{
  "symbol": "AAPL"
}
```

### Portfolio Analysis
- `POST /api/v1/portfolio/analyze` - Analyze portfolio

**Example Request**:
```json
{
  "portfolio": {
    "stocks": ["AAPL", "GOOGL", "MSFT"],
    "quantities": [10, 5, 8]
  },
  "value": 100000.0
}
```

### Allocation
- `POST /api/v1/allocation/analyze` - Get allocation recommendations

**Example Request**:
```json
{
  "portfolio": {
    "stocks": ["AAPL", "GOOGL"],
    "quantities": [10, 5]
  },
  "value": 50000.0
}
```

### Correlation Analysis
- `POST /api/v1/correlation/analyze` - Analyze stock correlations (POST)
- `GET /api/v1/correlation/analyze/{symbol}` - Analyze stock correlations (GET)

**Example Request (POST)**:
```json
{
  "symbol": "AAPL"
}
```

### Fundamental Reports
- `POST /api/v1/fundamental/report` - Get fundamental report (POST)
- `GET /api/v1/fundamental/report/{symbol}` - Get fundamental report (GET)

**Example Request (POST)**:
```json
{
  "symbol": "AAPL"
}

### Memory Analysis
- `POST /api/v1/memory/analyze` - Run memory analysis (POST)
- `GET /api/v1/memory/analyze/{symbol}` - Run memory analysis (GET)

**Example Request (POST)**:
```json
{
  "symbol": "AAPL"
}
```

### Explain Analysis
- `POST /api/v1/explain/analyze` - Run explain analysis (POST)
- `GET /api/v1/explain/analyze/{symbol}` - Run explain analysis (GET)

**Example Request (POST)**:
```json
{
  "symbol": "AAPL"
}
```
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
apis/
├── main.py                 # Main FastAPI application
├── config.py              # Configuration settings
├── __init__.py
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic request/response models
└── routers/
    ├── __init__.py
    ├── stock_router.py        # Stock analysis endpoints
    ├── portfolio_router.py    # Portfolio analysis endpoints
    ├── allocation_router.py   # Allocation endpoints
    ├── correlation_router.py  # Correlation analysis endpoints
    ├── fundamental_router.py  # Fundamental report endpoints
    ├── memory_router.py       # Memory analysis endpoints
    └── explain_router.py      # Explain analysis endpoints
```

## Configuration

Create a `.env` file in the project root to customize settings:

```env
API_TITLE=Stock Predictor API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

## Error Handling

All endpoints include proper error handling and return structured error responses:

```json
{
  "status": "error",
  "message": "Error description",
  "detail": "Detailed error information"
}
```

## Testing

Use curl, Postman, or the built-in Swagger UI to test endpoints.

**Example with curl**:
```bash
# Stock analysis
curl -X POST http://localhost:8000/api/v1/stock/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'

# Or using GET
curl http://localhost:8000/api/v1/stock/analyze/AAPL
```

## Notes

- All engines are initialized on-demand for each request
- Logging is configured to track all requests and errors
- CORS is enabled for all origins (configure for production use)
- The API uses async handlers for better performance
