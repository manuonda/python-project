import boto3
from botocore.exceptions import ClientError

def chat_with_bedrock():
    # 1. Configurar el cliente
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # 2. Elegir el modelo (La API Converse funciona con muchos modelos)
    # Ejemplos: "anthropic.claude-3-haiku-20240307-v1:0", "amazon.titan-text-express-v1", "meta.llama3-8b-instruct-v1:0"
    model_id = "amazon.titan-text-express-v1"

    # 3. Definir el historial de la conversación
    # La API Converse usa una lista de mensajes con roles 'user' o 'assistant'
    conversation = [
        {
            "role": "user",
            "content": [{"text": "Hola, soy un desarrollador de Python."}]
        },
        {
            "role": "assistant",
            "content": [{"text": "¡Hola! Es genial conocer a otro desarrollador. ¿En qué puedo ayudarte hoy con Python?"}]
        },
        {
            "role": "user",
            "content": [{"text": "¿Cuáles son las ventajas de usar la API Converse de Bedrock?"}]
        }
    ]

    temperature = 0.7
    top_k = 200

    print("Enviando conversación al modelo...")

    try:
        # 4. Llamar a la API Converse
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": temperature,  # Usamos la variable definida arriba
                "topP": 0.9
            },
            # 'top_k' no está en inferenceConfig estándar, se pasa como campo adicional
            # Nota: No todos los modelos soportan top_k (Titan sí, Claude también)
            additionalModelRequestFields={
                "top_k": top_k
            }
        )

        # 5. Procesar la respuesta
        output_message = response['output']['message']
        response_text = output_message['content'][0]['text']

        print("\n--- Respuesta del Modelo ---")
        print(f"Role: {output_message['role']}")
        print(f"Content: {response_text}")
        
        # Información adicional útil (tokens usados)
        usage = response['usage']
        print(f"\n--- Uso ---")
        print(f"Input tokens: {usage['inputTokens']}")
        print(f"Output tokens: {usage['outputTokens']}")

    except ClientError as e:
        print(f"ERROR: No se pudo invocar el modelo '{model_id}'. Razón: {e}")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

if __name__ == "__main__":
    chat_with_bedrock()
