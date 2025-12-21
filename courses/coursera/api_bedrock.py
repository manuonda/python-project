import boto3
import json

client = boto3.client('bedrock-runtime')

#api invoke model
response = client.invoke_model(    

     modelId='amazon.titan-text-express-v1',    

     body=json.dumps({        

          "inputText": "explain quantum computing",        

          "textGenerationConfig": {            

               "maxTokenCount": 100,            

               "temperature": 0.5,            

               "topP": 0.9        

          }    

     })

)

print(json.loads(response['body'].read()))

print(" ----- Response Stream  ------")
response = client.invoke_model_with_response_stream(    

     modelId='amazon.titan-text-express-v1',    

     body=json.dumps({        

          "inputText": "explain quantum computing",        

          "textGenerationConfig": {            

          "maxTokenCount": 200,            

          "temperature": 0.5,            

          "topP": 0.9        

     }    

  })

)

# Process the streaming response

for event in response.get('body'):    
     chunk = json.loads(event['chunk']['bytes'])    
     print(chunk['outputText'], end='', flush=True)


def safe_model_invoke(prompt, model_id):    
    try:        

        response = bedrock_runtime.invoke_model(            

              modelId=model_id,            

              body=json.dumps({                

                   "inputText": prompt,                

                   "textGenerationConfig": {                    

                        "maxTokenCount": 512,                    

                        "temperature": 0.7                

                    }            

              })        

         )        

        return json.loads(response['body'].read())    

    except bedrock_runtime.exceptions.ValidationException:        

         print("Invalid request parameters")    

    except bedrock_runtime.exceptions.ModelTimeoutException:        

         print("Model inference timed out")    

    except Exception as e:        

         print(f"Unexpected error: {str(e)}")