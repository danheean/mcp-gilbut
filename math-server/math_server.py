import logging

from mcp.server.fastmcp import FastMCP 

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Math")

@mcp.tool()
def add(a, b) -> int:
    """Add two numbers together"""
    try:
        a = int(a)
        b = int(b)
        logging.info(f"Adding {a} and {b}")
        return a + b
    except Exception as e:
        logging.error(f"Invalid input in add: {a} or {b} - {e}")
        raise

@mcp.tool()
def subtract(a, b) -> int:
    """Subtract two numbers together"""
    try:
        a = int(a)
        b = int(b)
        logging.info(f"Subtracting {a} and {b}")
        return a - b
    except Exception as e:
        logging.error(f"Invalid input in subtract: {a} or {b} - {e}")
        raise
if __name__ == "__main__":
    mcp.run(transport="stdio")