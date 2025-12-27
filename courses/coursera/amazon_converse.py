import boto3
import json
from botocore.exceptions import ClientError


#Es una capa de traducción universal. 
# Usas el mismo formato de mensajes para todos los modelos.
#Lo bueno: Puedes cambiar de amazon.titan a anthropic.claude solo cambiando el modelId, 
# sin tocar el resto del código.
#Lo bueno: Soporta Tool Use (uso de herramientas) y Guardrails de forma nativa y estandarizada.
# Lo bueno: Maneja el historial de chat (messages=[...]) de forma estructurada.

# Set the AWS Region
region = "us-east-1"

# Initialize the Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name=region)

# Define the model ID for Amazon Titan Express v1
model_id = "amazon.titan-text-express-v1"

messages = [
    {
        "role":"user",
        "content": [{"text":"Hola mi nombre Es David, soy un desarrollador de pyhton"}]
    },{
        "role":"assistant",
        "content":[{ "text" :"Hola. Es genial conocer a otro desarrollador. En que puedo ayudarte?"}]
    },{
        "role":"user",
        "content":[{"text":"Cuales son las ventajas de usar la API Converse de Bedrock?"}]
    }
]

system_prompt=[{"text":" Tu eres un asistente para desarrolladores"}]

temperature = 0.7
top_k = 200

inference_config = {
    "temperature":temperature,
    "maxTokens":512,
    "topP": 0.9
    }
# messages.append(system_prompt)  <-- ELIMINADO: No se debe agregar a messages

response = client.converse(
    modelId=model_id,
    messages=messages,
    # system=system_prompt,  <-- COMENTADO: Titan Text Express NO soporta system prompts
    inferenceConfig=inference_config
)

# output_message
# 5. Procesar la respuesta
output_message = response['output']['message']
response_text = output_message['content'][0]['text']

print("\n--- Respuesta del Modelo ---")
print(f"Role: {output_message['role']}")
print(f"Content: {response_text}")



# --- SEGUNDA VUELTA ---

# 1. Agregar la respuesta anterior del asistente al historial
messages.append(output_message)

# 2. Agregar la nueva pregunta del usuario
messages.append({
    "role": "user",
    "content": [{"text": "Cual es mi nombre de desarrollador que te dije al comenzar la charla?"}]
})

# 3. Llamar a la API nuevamente
response = client.converse(
    modelId=model_id,
    messages=messages,
    inferenceConfig=inference_config
)

output_message = response['output']['message']
response_text = output_message['content'][0]['text']

print("\n--- Respuesta del Modelo (2da vuelta) ---")
print(f"Role: {output_message['role']}")
print(f"Content: {response_text}")

# Información adicional útil (tokens usados)
usage = response['usage']
print(f"\n--- Uso ---")
print(f"Input tokens: {usage['inputTokens']}")
print(f"Output tokens: {usage['outputTokens']}")

