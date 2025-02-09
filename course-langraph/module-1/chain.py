from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

messages = [
    AIMessage(content=f"So you said you were researching ocean mammals?", name="Model"),
    HumanMessage(content=f" Yes that's right.", name="Lance"),
    AIMessage(content=f"Great, what would you like to learn about.", name="Model"),
    HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Lance")
]

llm = ChatOpenAI(model="gpt-4o")
result =llm.invoke(messages)
type(result)

print(result.content)
print("\n")
print(result.response_metadata)


### Add Tools
def multiply(a,b) ->int:
    return a* b

llm_with_tools = llm.bind_tools([multiply])
tool_call = llm_with_tools.invoke([HumanMessage(content=f"What is multiple 2 * 3")])
print("\n Tool call result ")
print(tool_call.tool_calls)

##langraph has pre-built MessageState!
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages

class MessagesState(MessagesState):
    pass


# initial state 
initial_messages = [
    AIMessage(content=f"Hello! How can I assist you?"),
    HumanMessage(content=f"I'm looking information or marine biology")
]

#new message to add
new_message = AIMessage(content=f"Sure, I can help with that.What specifically are you interested in?")


add_messages(initial_messages, new_message)

## graph
from langgraph.graph import StateGraph, START, END

#node with tools 
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

#Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)

#edges
builder.add_edge(START,"tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content="Hello!")})
for m in messages['messages']:
    m.pretty_print



print("\n Messages")
messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
for m in messages['messages']:
    m.pretty_print()