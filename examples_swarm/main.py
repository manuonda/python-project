from swarm import Swarm,Agent

client= Swarm()

english_client = Agent(
    name="English Agent",
    instructions="You only speak English",
)

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish",
)

def transfer_to_spanish_agent():
    """Transfer spanish speaking users immediately"""
    return spanish_agent
