import os

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
#load environment variables
load_dotenv()

#Configure logfire
logfire.configure()


## create a pydanticai instance
model = OpenAIModel('gpt-4o')
agent = Agent(model)

# run the agent
result = agent.run_sync("What is the capital of France?")
print(result)