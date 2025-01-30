from langgraph.graph import MessagesState
from langchain import Chain


class State(MessagesState):
    my_var:str


# definte the tools
def add(a: int , b: int) -> int:
    """ Add two numbers 
      
     Args:
        a (int): First number
        b (int): Second number
    """
    return a + b

def multiply(a: int , b: int) -> int:
    """ Multiply two numbers 
      
     Args:
        a (int): First number
        b (int): Second number
    """
    return a * b


tools = [multiply,add]

llm = ChatopenAI(model="gpt-4o", temperature=0)