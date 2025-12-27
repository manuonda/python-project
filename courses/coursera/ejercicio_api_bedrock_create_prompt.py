import boto3
import json
from botocore.exceptions import ClientError
temperature = .7


# Set the AWS Region
region = "us-east-1"

# Initialize the Bedrock Runtime client
bedrock = boto3.client("bedrock-runtime", region_name=region)

inference_config = {"temperature": temperature}

system_prompts = [{"text": "You are a virtual travel assistant that suggests destinations based on user preferences."
                + "Only return destination names and a brief description."}]

messages = []

message_1 = {
    "role": "user",
    "content": [{"text": "Create a list of 3 travel destinations."}]
}

messages.append(message_1)
model_id = "amazon.titan-text-express-v1"

response = bedrock.converse(
    modelId=model_id,
    messages=messages,
    #system=system_prompts,
    inferenceConfig=inference_config
)

def print_response(response):
    model_response = response.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', '')

    print("✈️ Your suggested travel destinations:")
    print(model_response)

print_response(response)



message_2 = {
        "role": "user",
        "content": [{"text": "Only suggest travel locations that are no more than one short flight away."}]
}

messages.append(message_2)

response = bedrock.converse(
    modelId=model_id,
    messages=messages,
    #system=system_prompts,
    inferenceConfig=inference_config
)

print_response(response)


message_3 = {
        "role": "user",
        "content": [{"text": "INSERT YOUR PROMPT HERE"}]
}

messages.append(message_3)

response = bedrock.converse(
    modelId=model_id,
    messages=messages,
    #system=system_prompts,
    inferenceConfig=inference_config
)

print_response(response)