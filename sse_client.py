import asyncio
import sys
import json 

from mcp import ClientSession 
from mcp.client.sse import sse_client

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py http://127.0.0.1:3000/sse")
        return

    url = sys.argv[1]
    print(f"[클라이언트] 서버에 SSE 연결 시도 중...({url})")
    async with sse_client(url) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            print(f"MCP Chat Client 시작됨. 'quit' 입력 시 종료됩니다.")

            while True:
                user_input = input("\nQuery: ").strip()

                if user_input.lower() == "quit":
                    break

                try:
                    response = await session.call_tool("chat", {"input": user_input})

                    print("type(response):", type(response))

                    if isinstance(response.content, str):
                        try:
                            data = json.loads(response.content)
                            print("\n GPT-4o 응답1:\n" + data["content"])
                        except json.JSONDecodeError:
                            print("\n GPT-4o 응답2:\n" + response.content)
                    elif isinstance(response.content, dict):
                        print("\n GPT-4o 응답3:\n" + response.content.get("content", str(response.content)))
                    else:
                        print("\n GPT-4o 응답4:\n" + str(response.content))

                except Exception as e:
                    print(f"\n 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())