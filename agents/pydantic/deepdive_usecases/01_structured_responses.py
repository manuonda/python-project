import os

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
#load environment variables
load_dotenv()

#Configure logfire
logfire.configure()

#Define a Pydantic model for the intent 
class Intent(BaseModel):
    intent:str


model = OpenAIModel('gpt-4o')
agent = Agent(
    model,
    system_prompt=(
        "You are a helpful ai assistant"
        "Identify thye user's from the provided options"
        "Choose from thes options: 'getTasks', 'MarkTaskAsDone', 'CreateTask', 'DeleteTask'"),
    result_type=Intent,
    result_retries=3
)

## validator for the agent once a result is returned 
## this will validate the intent and raise a ModelRetry exception if the intent is not valid
@agent.result_validator
def validate_intent(ctx: RunContext[None], result: Intent) -> Intent:
    if result.intent not in ['getTasks', 'MarkTaskAsDone', 'CreateTaskz', 'DeleteTaskz']:
        raise ModelRetry("Invalid Intent Provider. Please choose from the provided options")
    return result

result = agent.run_sync("I just got done with my groceries")
print(result.data)