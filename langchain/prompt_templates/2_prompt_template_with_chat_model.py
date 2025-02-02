from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# load environments
load_dotenv()

#Create models 
model = ChatOpenAI(model="gpt-4o")

# Part 1: Crate a ChatPromptTemplate using a template string
print("--- Prompt from Template ----")
template = "Tell me a joke about {topic}"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"topic": "cats"})
result = model.invoke(prompt)
print(result.content)


# Part 2 : Prompt with multiple placeholders
print("\n--- Prompt with multiple placeholders ----")
template_multipe= """ You are a helpful assistant 
Human: Tell me a {adjective} short story about a {animal}
Assistant:"""
prompt_template = ChatPromptTemplate.from_template(template_multipe)
prompt = prompt_template.invoke({"adjective":"funny", "animal":"panda"})
result = model.invoke(prompt)
print(result.content)

#Parte 3 : Prompt with System and humman messagee
print("\n--- Prompt with System and Human Messages(Tuple)----")
messages = [
    ("system","You are a comedian who tells jokes about {topic}"),
    ("human","Tell me a {joke_count} jokes")
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic":"lawyers","joke_count":3})
result = model.invoke(prompt)
print(result.content)



