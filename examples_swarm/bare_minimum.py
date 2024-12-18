from swarm import Swarm,Agent
from dotenv import load_dotenv
import os
load_dotenv()


client = Swarm()

agent = Agent(
  name="Agent",
  instructions="You are in expert in anime"
)

messages = [{"role":"user", "content":"Hola soy fan de naruto"}]
response = client.run(
    agent=agent,
    messages=messages
)

print(response.messages[-1]["content"])