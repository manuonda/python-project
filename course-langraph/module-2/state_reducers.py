from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    foo: int

def node_1(state):
    print("---Node 1---")
    result = state['foo'] + 1
    print("result node 1 {}", result)
    return {"foo": result}

def node_2(state):
    print("---Node 2---")
    result = state['foo'] + 1
    print("result node 2 {}", result)
    return {"foo": result}

def node_3(state):
    print("---Node 3---")
    result = state['foo'] + 1
    print("result node 3 {}", result)
    return {"foo": result}

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

from langgraph.errors import InvalidUpdateError
try:
    graph.invoke({"foo" : 1})
except InvalidUpdateError as e:
    print(f"InvalidUpdateError occurred: {e}")