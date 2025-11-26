import boto3
import json
from botocore.exceptions import ClientError

# Set the AWS Region
region = "us-east-1"

# Initialize the Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name=region)

# Define the model ID for Amazon Titan Express v1
model_id = "amazon.titan-text-express-v1"

def generate_stream(prompt):
    print(f"\n Prompt:{prompt}")
    print("Response: ", end="", flush=True)

    inference_parameters={
        "inputText": prompt,
        "textGenerationConfig":{
            "maxTokenCount":100,
            "temperature":0.5
        }
    }

    request_payload = json.dumps(inference_parameters)

    try:
        # Invoke the model with streaming
        response = client.invoke_model_with_response_stream(
            modelId=model_id,
            body=request_payload,
            contentType="application/json",
            accept="application/json"
        )

        # Process the stream
        for event in response.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])
            if "outputText" in chunk:
                print(chunk["outputText"], end="", flush=True)
        print() # New line at the end

    except ClientError as e:
        print(f"\nClientError: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    prompt_text="Naruto shipudden"
    generate_stream(prompt_text) 