"""
Quick start script for the FastMCP Stock Predictor tools server.
"""
import os
import sys

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apis.logging_config import setup_logging

if __name__ == "__main__":
    from apis.mcp_server import create_mcp_server, get_available_profiles
    logger = setup_logging("stock-predictor-mcp-launcher")
    profile = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MCP_AGENT_PROFILE")

    if not profile:
        available_profiles = ", ".join(get_available_profiles())
        raise SystemExit(
            "Missing MCP profile. Start with 'python apis/start_mcp_server.py <profile>' "
            f"or set MCP_AGENT_PROFILE. Available profiles: {available_profiles}"
        )

    mcp = create_mcp_server(profile)

    print(
        f"""
╔═══════════════════════════════════════════════════════╗
║   Stock Predictor MCP Tools Server                    ║
╚═══════════════════════════════════════════════════════╝

Starting MCP server over stdio...
Profile: {profile}
Use this command in your MCP client config:
python apis/start_mcp_server.py {profile}

Available profiles:
{', '.join(get_available_profiles())}

Press CTRL+C to stop the server.
"""
    )

    logger.info("Launching MCP server with stdio transport for profile=%s", profile)
    mcp.run(transport="stdio")
