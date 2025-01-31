from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


#load environment variables from .env
load_dotenv()

# model
model = ChatOpenAI(model="gpt-4o")

chat_history = [] # use a list to store messages

# set a initial message
system_message =SystemMessage(content="You are a helpful assistant")
chat_history.append(system_message)

#Chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    #Get AI response with using history 
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print(f"AI: {response}")


print("-- Messages History --")
print(chat_history)