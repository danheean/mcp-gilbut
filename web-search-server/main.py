import os
import logging

# 로깅 설정 강화
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_search_debug.log'),
        logging.StreamHandler()
    ]
)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import requests

from mcp.server.fastmcp import FastMCP

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

mcp = FastMCP("WebSearch")

def search_web_tavily(query: str) -> str:
    url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 5,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            return "검색 결과가 없습니다."
        
        contents = "\n\n".join([f"{r['title']}\n{r['content']}" for r in results])
        return contents
    except Exception as e:
        logging.error(f"Tavily Web 검색 오류: {e}")
        return f"Tavily Web 검색 오류: {e}"
    
@mcp.tool()
async def web_search(query: str) -> str:
    """웹에서 검색한 결과를 요약해 제공합니다."""
    logging.info(f"Web 검색 요청: {query}")
    
    contents = search_web_tavily(query)
    logging.debug(f"검색 결과: {contents[:200]}...")  # 처음 200자만 로깅
    
    summary = await llm.ainvoke(f"다음 검색 결과를 한 문단으로 요약해줘: \n\n{contents}")
    logging.info(f"요약 완료: {summary.content[:100]}...")
    return summary.content

if __name__ == "__main__":
    mcp.run(transport="stdio")