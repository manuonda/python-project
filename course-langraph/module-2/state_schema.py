import random
from typing_extensions import TypedDict
from typing import Literal

from dataclasses import dataclass
from pydantic import BaseModel, field_validator, ValidationError



#langgrap
from langgraph.graph import StateGraph, START, END


# @dataclass
# class DataClassState:
#     name: str
#     mood : Literal["happy","sad"]



# class TypedicState(TypedDict):
#     name: str
#     mood: Literal["happy","sad"]

class PydanticState(BaseModel):
    name: str
    mood: str # "happy" or "sad"
    
    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        #Ensure the mood is either "happy" or "sad":
        if value not in ["happy","sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value
try:
    state = PydanticState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)
    



def node_1(state):
    print("--Node 1 ---")
    return {"name": state.name + "is..."}    


def node_2(state):
    print("--Node 2 ---")
    return {"mood":"happy"}

def node_3(state):
    print("--Node 3---")
    return {"mood":"sad"}


def decide_mood(state)->Literal["node_2","node_3"]:
    if random.random() < 0.5:
        print("probabilty  < 0.5")
        return "node_2"
    
    print("probabilty > 0.5")
    return "node_3"


#build graph 
builder = StateGraph(DataClassState)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

#logic 
builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1",decide_mood)
builder.add_edge("node_2",END)
builder.add_edge("node_3",END)

graph = builder.compile()

result = graph.invoke({"name":"David Garcia"})
print(result)

