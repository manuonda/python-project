from swarm import Agent
from configs.prompts import *

triage_agent = Agent(
  name="Triage Agent",
  instructions=triage_instructions(context_variables),
  functions=[
      switch_to_availability_agent,
      switch_to_cancellation_agent,
      switch_to_reviews_agent
  ]
)