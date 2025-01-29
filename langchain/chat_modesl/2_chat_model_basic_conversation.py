from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

#Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")


