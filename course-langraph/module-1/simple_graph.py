from typing_extensions import TypedDict
import random 
from typing import Literal
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

#Define the state
class State(TypedDict):
    graph_state: str
    
# define the nodes
def node_1(state):
    print("--Node 1---")
    return { "graph_state": state['graph_state'] + " I am "}


def node_2(state):
    print("--Node 2---")
    return {"graph_state": state["graph_state"] + " happy!"}

def node_3(state):
    print("--Node 3--")
    return {"graph_state": state["graph_state"] + " sad!"}



#Edges 
# Literal: define dentro del conjunto de valores que valor definir
def decide_mood(state) -> Literal['node_2', 'node_3']:
    
    #often , we will use state to decide on 
    # the next node to visit 
    user_input = state['graph_state']
    
    #Here, let's just do a 50/50 spllit beetween nodes 2, 3
    if random.random() < 0.5:
        return "node_2"
    
    #50% of the time, we return node 3 
    return "node_3"


#Graph construction 

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

#Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

#logic 
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)


#Add
graph = builder.compile()

#View 
display(Image(graph.get_graph().draw_mermaid_png()))

    
result = graph.invoke({"graph_state":"Hi my name is Lance!"})
print(result)