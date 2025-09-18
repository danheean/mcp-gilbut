import asyncio
from mcp_server import ask_gpt

async def client():
    question = "mcp와 agent의 관계를 알려줘"

    result = await ask_gpt(None, question)
    print("댭변:", result)


if __name__ == "__main__":
    asyncio.run(client())