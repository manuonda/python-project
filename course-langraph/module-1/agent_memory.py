from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

#graph 
from langgraph.graph import  START, END, StateGraph , MessagesState
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from dotenv import load_dotenv

load_dotenv()

#load environment
load_dotenv()


#Tools
@tool
def divide(a: float ,b:float) -> float:
    """ Divide two numbers and return flota value
    Args:
     a: float, 
     b: float
    """
    return a / b

@tool
def multiply(a: int, b:int) -> int:
    """ 
    Function que permite multiplicar 
    2 valores
    
    Args:
      a:int
      b:int
    """
    return a * b

@tool
def add(a:int , b:int) -> int:
    """ Function que permite sumar 2 valores
    Args:
     a: int 
     b: int
    """
    return a + b

#tools
tools = [multiply, add, divide]

#load models
llm = ChatOpenAI(model="gpt-4o")
#bind tools
llm_with_tools = llm.bind_tools(tools)


#System message
sys_msg = SystemMessage(content="You are a helpul assistant tasked with performing aritmetic on a set inputs")


#define node
def assitant(state:MessagesState):
    return {"messages": [llm_with_tools.invoke( [sys_msg] + state["messages"])]}

#define Graph 
builder = StateGraph(MessagesState)
builder.add_node("assistant", assitant)
builder.add_node("tools", ToolNode(tools))

#define edges
builder.add_edge(START,"assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message(result) from assistante is a tool call -> tools_condition route to tools 
    #If the latest message(result) from assitant is a not a tool call -> tools_condition routes to END
    tools_condition
)
builder.add_edge("tools", "assistant")

# memory 
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer= memory)

# When we use memory, we need to specify a thread_id.
#This thread_id will store our collection of graph states.

#specify a thread
config = {"configurable": {"thread_id":"1"}}

#specify an input 
messages = [HumanMessage(content="Add 3 and 4")]

#Run 
messages = react_graph_memory.invoke({"messages":messages},config)
for m in messages['messages']:
   m.pretty_print()

messages = [HumanMessage(content="Multiply that by 2.")]
messages = react_graph_memory.invoke({"messages": messages}, config)
for m in messages['messages']:
    m.pretty_print()
 
