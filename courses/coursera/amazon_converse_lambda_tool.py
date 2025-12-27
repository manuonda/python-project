import boto3
import json
from botocore.exceptions import ClientError

# Configuración
# Usamos Titan Text Express o Claude 3 Sonnet si está disponible. 
# Titan soporta tool use, pero Claude suele ser más robusto para seguir instrucciones complejas.
MODEL_ID = "amazon.nova-micro-v1:0" 
LAMBDA_ARN = ""
LAMBDA_REGION = "sa-east-1" # La región donde está desplegada la Lambda

# Inicializar clientes
# Bedrock Runtime (para Converse)
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
# Lambda (para invocar la herramienta)
lambda_client = boto3.client("lambda", region_name=LAMBDA_REGION)

def get_tool_config():
    """Define la configuración de la herramienta para Bedrock"""
    return {
        "tools": [
            {
                "toolSpec": {
                    "name": "get_weather",
                    "description": "Obtiene el clima actual (temperatura y condición) para una ubicación dada por latitud y longitud.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "lat": {
                                    "type": "string",
                                    "description": "La latitud de la ubicación geográfica (ej. 40.7128)"
                                },
                                "lon": {
                                    "type": "string",
                                    "description": "La longitud de la ubicación geográfica (ej. -74.0060)"
                                }
                            },
                            "required": ["lat", "lon"]
                        }
                    }
                }
            }
        ]
    }

def invoke_weather_lambda(lat, lon):
    """
    Invoca la función Lambda específica que actúa como herramienta.
    """
    payload = {
        "lat": lat,
        "lon": lon
    }
    
    print(f"   ⚡ Invocando Lambda ({LAMBDA_ARN})...")
    try:
        response = lambda_client.invoke(
            FunctionName=LAMBDA_ARN,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        # Leer el stream de respuesta
        response_payload = json.loads(response['Payload'].read())
        
        # La Lambda devuelve una estructura API Gateway { "statusCode": ..., "body": "..." }
        if response_payload.get('statusCode') == 200:
            # El body es un string JSON, necesitamos parsearlo para obtener el objeto real
            weather_data = json.loads(response_payload['body'])
            return weather_data
        else:
            error_msg = response_payload.get('body', 'Error desconocido en Lambda')
            return {"error": f"Lambda falló: {error_msg}"}
            
    except Exception as e:
        return {"error": f"Error invocando Lambda: {str(e)}"}

def main():
    print("--- Demo: Bedrock Converse API + Tool Use (AWS Lambda) ---")
    
    # Definimos la herramienta
    tool_config = get_tool_config()
    
    # Mensaje inicial del usuario
    # Nota: Incluimos coordenadas para facilitar la demo, ya que la tool requiere lat/lon
    user_input = "¿Cómo está el clima en Nueva York hoy? (Lat: 40.7128, Lon: -74.0060)"
    
    messages = [
        {"role": "user", "content": [{"text": user_input}]}
    ]
    
    print(f"\nUsuario: {user_input}")

    try:
        # 1. Primera llamada a Bedrock (Pensamiento y decisión de uso de herramienta)
        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig=tool_config
        )
        
        output_message = response['output']['message']
        messages.append(output_message) # Actualizar historial
        
        stop_reason = response['stopReason']
        
        if stop_reason == 'tool_use':
            print("\n🤖 El modelo ha decidido usar una herramienta.")
            
            tool_results = []
            
            # Iterar sobre los bloques de contenido para encontrar solicitudes de uso de herramienta
            for content_block in output_message['content']:
                if 'toolUse' in content_block:
                    tool_use = content_block['toolUse']
                    tool_id = tool_use['toolUseId']
                    tool_name = tool_use['name']
                    tool_input = tool_use['input']
                    
                    print(f"   Herramienta solicitada: {tool_name}")
                    print(f"   Parámetros: {tool_input}")
                    
                    if tool_name == 'get_weather':
                        # AQUI es donde ocurre la integración:
                        # 1. Bedrock nos dijo: "Necesito ejecutar la herramienta 'get_weather'"
                        # 2. Nosotros verificamos el nombre y llamamos a la función local correspondiente
                        # 3. La función local 'invoke_weather_lambda' usa boto3 para llamar a la Lambda real
                        print(f"   🚀 Bedrock solicitó '{tool_name}' -> Ejecutando cliente Lambda...")
                        
                        lat = str(tool_input.get('lat'))
                        lon = str(tool_input.get('lon'))
                        
                        tool_result_data = invoke_weather_lambda(lat, lon)
                        print(f"   Resultado obtenido: {tool_result_data}")
                        
                        # Construir la respuesta de la herramienta para Bedrock
                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_id,
                                "content": [
                                    {"json": tool_result_data}
                                ]
                            }
                        })
            
            # 2. Enviar los resultados de la herramienta de vuelta al modelo
            if tool_results:
                # Añadir mensaje con los resultados de las herramientas
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                print("\n🔄 Enviando resultados al modelo para respuesta final...")
                
                # Segunda llamada a Bedrock (Generación de respuesta final)
                final_response = bedrock_client.converse(
                    modelId=MODEL_ID,
                    messages=messages,
                    toolConfig=tool_config
                )
                
                final_text = final_response['output']['message']['content'][0]['text']
                print(f"\n🤖 Respuesta Final:\n{final_text}")
                
        else:
            print(f"\nEl modelo respondió directamente (Stop Reason: {stop_reason}):")
            print(output_message['content'][0]['text'])

    except ClientError as e:
        print(f"❌ Error de AWS: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 
#Lambda function named getWeather already created

