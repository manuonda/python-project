from typing import TypedDict

#Define the state of the agent

class State(TypedDict):
    my_var: str
    customer_name: str


#Define nodes(agent  == nodes )

def nodes_1(state: State) -> State: 
    state['my_var'] = "Hello"
    state["customer_name"] = "Jhon"
    return state

def node_2(state: State)-> State:
    customer_name = state["customer_name"]
    