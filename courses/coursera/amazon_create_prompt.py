import boto3
import json
from botocore.exceptions import ClientError

def create_prompt_example():
    """
    Crea un Prompt en Amazon Bedrock Prompt Management.
    """
    # Verificar identidad
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    print(f"🔑 Identidad actual: {identity['Arn']}")
    print(f"   Account: {identity['Account']}")

    # Inicializar el cliente de Bedrock Agent (donde vive Prompt Management)
    client = boto3.client("bedrock-agent", region_name="us-east-1")

    prompt_name = "ResumidorDeTexto"
    description = "Un prompt para resumir textos usando Titan"
    
    print(f"Creando prompt '{prompt_name}'...")

    response = None
    try:
        response = client.create_prompt(
            name=prompt_name,
            description=description,
            variants=[
                {
                    "name": "variante-titan",
                    "templateType": "TEXT",
                    "templateConfiguration": {
                        "text": {
                            # Las variables se definen con doble llave {{variable}}
                            "text": "Por favor resume el siguiente texto en 3 oraciones:\n\n{{texto_entrada}}",
                            "inputVariables": [
                                {
                                    "name": "texto_entrada"
                                }
                            ]
                        }
                    },
                    # ID del modelo que usará este prompt por defecto
                    "modelId": "amazon.titan-text-express-v1",
                    "inferenceConfiguration": {
                        "text": {
                            "temperature": 0.5,
                            "maxTokens": 512,
                            "topP": 0.9
                        }
                    }
                }
            ]
        )
        print("✅ Prompt creado exitosamente!")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConflictException':
            print(f"⚠️ El prompt '{prompt_name}' ya existe. Recuperando información...")
            # Listar prompts para encontrar el ID
            paginator = client.get_paginator('list_prompts')
            for page in paginator.paginate():
                for p in page['promptSummaries']:
                    if p['name'] == prompt_name:
                        # Obtener detalles completos
                        response = client.get_prompt(promptIdentifier=p['id'])
                        break
                if response: break
            
            if not response:
                print("❌ No se pudo encontrar el prompt existente.")
                return None
        else:
            print(f"❌ Error al crear el prompt: {e}")
            return None

    if response:
        prompt_arn = response['arn']
        prompt_id = response['id']
        
        print(f"ID: {prompt_id}")
        print(f"ARN: {prompt_arn}")
        
        # --- CÓMO USAR EL PROMPT CREADO ---
        if prompt_arn:
            print("\n--- Probando el Prompt ---")
            
            # 1. Necesitamos el cliente de Runtime para ejecutar el modelo
            runtime_client = boto3.client("bedrock-runtime", region_name="us-east-1")
            
            # 2. Recuperar la definición del prompt (si no la tuviéramos ya)
            # En un caso real, usarías client.get_prompt(promptIdentifier=prompt_id)
            
            # 3. Preparar el texto reemplazando la variable
            # El template es: "Por favor resume el siguiente texto en 3 oraciones:\n\n{{texto_entrada}}"
            texto_para_resumir = "Amazon Bedrock es un servicio totalmente gestionado que ofrece una selección de modelos fundacionales (FM) de alto rendimiento de las principales empresas de IA, como AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI y Amazon, a través de una única API, junto con un amplio conjunto de capacidades que necesita para crear aplicaciones de IA generativa con seguridad, privacidad y IA responsable."
            
            # Obtenemos el template de la respuesta de creación (o de get_prompt)
            template_text = response['variants'][0]['templateConfiguration']['text']['text']
            
            # Reemplazo manual de la variable (Bedrock Prompt Management no hace el reemplazo en el runtime por ti en esta API)
            final_prompt = template_text.replace("{{texto_entrada}}", texto_para_resumir)
            
            print(f"Prompt final enviado al modelo:\n{final_prompt}\n")
            
            # 4. Ejecutar con Converse
            model_id = response['variants'][0]['modelId'] # Usamos el modelo definido en el prompt
            
            response_converse = runtime_client.converse(
                modelId=model_id,
                messages=[{
                    "role": "user",
                    "content": [{"text": final_prompt}]
                }],
                inferenceConfig={
                    "temperature": 0.5,
                    "maxTokens": 50
                }
            )
            
            print("Respuesta del modelo:")
            print(response_converse['output']['message']['content'][0]['text'])

        return response['id']

if __name__ == "__main__":
    create_prompt_example()
