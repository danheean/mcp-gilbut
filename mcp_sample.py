from mcp.server.fastmcp import FastMCP
import logging
import asyncio 

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="stdio"))