import os 
from dataclasses import dataclass

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# load environment variables
load_dotenv()

#Configure logfire
logfire.configure()

@dataclass
class MyDeps:
    name: str