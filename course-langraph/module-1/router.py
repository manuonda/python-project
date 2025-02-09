import os, getpass
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def multiply(a: int, b:int) -> int:
    """ Multiply a and b 
       
        Args:
          a: first int 
          b: second int
    """
    return a * b

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([multiply])

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

#Node 
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

#build graph 
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
#ToolNode 
builder.add_node("tools", ToolNode([multiply]))

#edges
builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    #if the latest message(result) from assistant is a tool call -> tools_conditions routes to tools 
    #if the latest message(result) from assistant is a not a tool call -> tools_conditions routes to End
    tools_condition
)

builder.add_edge("tools",END)
graph = builder.compile()


from langchain_core.messages import HumanMessage
messages = [HumanMessage(content="Hello,mi nombre es David? .")]
messages = graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()


