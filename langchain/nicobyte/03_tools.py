import os 
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
resp = llm.invoke("cuanto es 12 * 2")
print(resp)




def multiply(a: int , b: int) -> int:
    """ Multiply two numbers 
      
     Args:
        a (int): First number
        b (int): Second number
    """
    return a * b

def add(a: int , b: int) -> int:
    """ Add two numbers 
      
     Args:
        a (int): First number
        b (int): Second number
    """
    return a + b


tools = [multiply,add]

## que no llame varias funciones paralelas
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls = False)


resp_with_tools = llm_with_tools.invoke("Hola como te llamas?")
print(" **** With tools pero no llama a las tools ********")
print(resp_with_tools)


print(" **** with tools  add *********")
resp_with_tools_2 = llm_with_tools.invoke("cuanto veces es cinco 43")
print(resp_with_tools_2)


print(" *** no corresponde *****")
resp_with_tools_3 = llm_with_tools.invoke("cuanto es una pera por una manzana")
print(resp_with_tools_3)