from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

#Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")


# SystemMessage: Este tipo de mensaje se utiliza para proporcionar 
# instrucciones o contexto al modelo de lenguaje. 
# No es parte de la conversación entre el usuario y el modelo, 
# sino que establece el escenario o las reglas para la interacción.

# HumanMessage: Este tipo de mensaje 
# representa la entrada del usuario. 
# Es lo que el usuario escribe o dice al modelo de lenguaje.


# AIMessage: Este tipo de mensaje representa la respuesta generada por el modelo de lenguaje. 
# Es la salida del modelo basada en los mensajes del sistema y del usuario proporcionados.
# PromptMessage: Este tipo de mensaje es una combinación de mensajes del sistema y mensajes humanos que se utilizan para generar una respuesta del modelo de lenguaje. Es el prompt completo que se envía al modelo para obtener una respuesta. 
messages= [
    SystemMessage(content="Solve the following math problems "),
    HumanMessage(content="What is 2+2?"),
    AIMessage(content="81 divided by 9 is 9."),
    HumanMessage(content="What is 2*2?"),
]

#Invoke the model with messages 
response = model.invoke(messages)
print(f"Answer from AI:  {response.content}")


