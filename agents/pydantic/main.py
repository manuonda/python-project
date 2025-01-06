from pydantic_ai import Agent, RunContext


roulette_agent = Agent(
   model='openai:gpt-4o',
   system_prompt=(
       'You are a friendly assistant'
   )
)

usr_msg = "What is the cappital of France?"
result = roulette_agent.run_sync(usr_msg)
print(result)

while usr_msg != "quit":
    print(f'Resultado: {result.data}')
    usr_msg = input(">")
    result = roulette_agent.run_sync(usr_msg, message_history=result.all_messages())
