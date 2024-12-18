from swarm import Swarm , Agent
from dotenv import load_dotenv
import os 

load_dotenv()


client = Swarm()

def instructions(context_variables):
    name= context_variables.get("name","User")
    return f"You are a helpful agent. Greet the user by name ({name})"


def print_account_details(context_variables: dict):
    user_id = context_variables.get("user_id", None)
    name = context_variables.get("name", None)
    print(f"Account Details: {name} {user_id}")
    return "Success"

def send_email(context_variables: dict):
    recipient = context_variables.get("recipient", None)
    subject = context_variables.get("subject", None)
    body = context_variables.get("body", None)
    return "Email sent successfully."

agent = Agent(
    name="Agent",
    instructions=instructions,
    functions=[print_account_details , send_email]
)

context_variables = {"name":"David","user_id":"1" ,
                     "email":"manuonda@gmail.com",
                     "recipient":"que onda","subject":"prueba envio email",
                     "body":"Hola mundo!"}

response = client.run(
    messages=[{"role":"user","content":"Hi!"}],
    agent=agent,
    context_variables=context_variables

)
print(response.messages[-1]["content"])

response = client.run(
    messages=[{"role": "user", "content": "Print my account details!"}],
    agent=agent,
    context_variables=context_variables,
)

response = client.run(
    messages=[{"role": "user", "content": "Send email"}],
    agent=agent,
    context_variables=context_variables,
)
print(response.messages[-1]["content"])