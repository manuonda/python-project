from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode



@tool
def multiply(a: int, b:int) -> int:
    return a * b

@tool
def add(a:int , b:int) -> int:
    return a + b

llm = ChatOpenAI(model="gpt-4o")
llm_tool = llm.bind_tools([multiply, add])
tool_node = ToolNode

