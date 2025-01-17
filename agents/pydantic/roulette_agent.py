from pydantic_ai import Agent, RunContext


roulette_agent = Agent(
    model='openai:gpt-4o-mini',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the ``roulette_wheel` function to see if the '
        'customer has won based on the number they have chosen.'
    )
)

@roulette_agent.tool(retries=3a)
async def roulette_wheel(ctx: RunContext[int], square :int ) -> str : 
    """ check if the square is a winner """
    return 'winner' if square == ctx.value else 'loser'

#Run the agent 
success_number = 19
result = roulette_agent.run_sync('Put my money on 19', deps=success_number)
print(result.data)

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)