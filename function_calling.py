import os 
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool 
def add(a: int, b:int) -> int:
    """Add two numbers together"""
    return a + b

@tool
def subtract(a: int, b:int) -> int:
    """Subtract two numbers"""
    return a - b

tools = [add, subtract]

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
)

response = agent.invoke("7에서 3을 빼줘")

print("응답:", response)
