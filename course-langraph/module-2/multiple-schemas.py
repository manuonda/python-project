from typing_extensions import TypedDict
from langgraph.graph  import StateGraph,START, END

class OverallState(TypedDict):
    foo :int 

class PrivateState(TypedDict):
    baz:int 


def node_1(state: OverallState) ->PrivateState:
    print("---Node 1--- ")
    print(state['foo'])
    return {"baz" :state['foo'] + 1}

def node_2(state: PrivateState) -> OverallState:
    print("---Node 2 ----")
    print(state['baz'])
    return {"foo": state['baz'] + 1}


 # Build graph
builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add
graph = builder.compile()

result = graph.invoke({"foo" : 1 })
print(result)

### Input / Output Schema 

print("\n Input / Output Schema --- ")
class OverallState2(TypedDict):
    question: str
    answer: str
    notes: str 

def thinking_node(state: OverallState2):
    return {"answer":"bye", "notes": "... his name is Lance"}

def answer_node(state: OverallState2):
    return {"answer":"bye Lance"}

graph2 = StateGraph(OverallState2)
graph2.add_node("answer_node", answer_node)
graph2.add_node("thinking_node",thinking_node)
graph2.add_edge(START ,"thinking_node")
graph2.add_edge("thinking_node","answer_node")
graph2.add_edge("answer_node",END)

graph2 = graph2.compile()
print(graph2.invoke({"question":"hi"}))


print("\n Specific input/output state ---")
class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    question: str
    answer: str
    notes: str

def thinking_node(state: InputState):
    return {"answer": "bye", "notes": "... his is name is Lance"}

def answer_node(state: OverallState) -> OutputState:
    return {"answer": "bye Lance"}

graph3 = StateGraph(OverallState, input=InputState, output=OutputState)
graph3.add_node("answer_node", answer_node)
graph3.add_node("thinking_node", thinking_node)
graph3.add_edge(START, "thinking_node")
graph3.add_edge("thinking_node", "answer_node")
graph3.add_edge("answer_node", END)

graph4 = graph3.compile()


print(graph4.invoke({"question":"hi"}))
