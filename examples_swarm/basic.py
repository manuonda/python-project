from swarm import Swarm,Agent
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API de OpenAI desde las variables de entorno
api_key = os.getenv('OPENAI_API_KEY')


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


english_client.functions.append(transfer_to_spanish_agent)

messages = [{"role": "user", "content":"Cual es el personaje de naruto?"}]
response = client.run(agent=english_client, messages = messages)

print(response.messages[-1]["content"])

