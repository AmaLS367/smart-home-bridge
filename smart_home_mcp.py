"""
FastMCP server for Smart Home Integration.
"""
from mcp.server.fastmcp import FastMCP
from smart_home import chromecast
from smart_home import ble_scales

# Initialize FastMCP server
mcp = FastMCP("Smart Home Bridge")

if __name__ == "__main__":
    mcp.run()
