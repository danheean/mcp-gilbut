from mcp.server.fastmcp import FastMCP, Context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("GPT-4o MCP")

llm = ChatOpenAI(model="gpt-4o", temperature=0)

@mcp.tool()
async def ask_gpt(ctx: Context, question: str) -> str:
    """Ask GPT-4o a question"""
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.3)
    response = await llm.ainvoke(question)
    return response

if __name__ == "__main__":
    mcp.run(transport="stdio")