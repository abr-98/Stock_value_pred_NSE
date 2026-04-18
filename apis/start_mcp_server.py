"""
Quick start script for the FastMCP Stock Predictor tools server.
"""
import os
import sys

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    from apis.mcp_server import mcp

    print(
        """
╔═══════════════════════════════════════════════════════╗
║   Stock Predictor MCP Tools Server                    ║
╚═══════════════════════════════════════════════════════╝

Starting MCP server over stdio...
Use this command in your MCP client config:
python apis/start_mcp_server.py

Press CTRL+C to stop the server.
"""
    )

    mcp.run(transport="stdio")
