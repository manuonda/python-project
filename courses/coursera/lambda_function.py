import json 
import urllib.request
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def lambda_handler(event, context):
    lat = event.get("lat")
    lon = event.get("lon")

    if not lat or not lon:
        return {
            "statusCode": 400,
            "body": json.dumps("Faltan parámetros lat o lon")
        }
    
    if not API_KEY:
        return {
            "statusCode": 500,
            "body": json.dumps("Falta la API Key de OpenWeather")
        }

    # Construir la URL (Current Weather Data)
    # Cambiamos a la API 2.5/weather para obtener el nombre de la ciudad ('name') y estructura 'main'
    # units=imperial: para grados Fahrenheit
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial&lang=es"

    try:
        # Realizar la petición HTTP usando urllib (nativo en Lambda)
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                
                # Extraer los datos solicitados
                result = {
                    "location": data.get("name", "Unknown location"),
                    "temperature": f"{data['main']['temp']}F",
                    "condition": data['weather'][0]['description'].title()
                }
                
                return {
                    "statusCode": 200,
                    "body": json.dumps(result)
                }
            else:
                return {
                    "statusCode": response.getcode(),
                    "body": json.dumps("Error en la respuesta de la API")
                }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error interno: {str(e)}")
        }