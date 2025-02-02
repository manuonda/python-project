from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# load environments 
load_dotenv()

# PART 1: Create a ChatPromptTemplate using a template string 
# template = "Tell me a joke about {topic}."
# prompt_template = ChatPromptTemplate.from_template(template)

# print("--- Promt from Template ----")
# prompt = prompt_template.invoke({"topic":"dog"})
# print(prompt)

# PART 2 : Prompt with multiple placeholders
# template_multiple =""" You are a helpful assitant
# Human: Tell me a {adjective} story about a {animal}
# Assitant:"""

# prompt_multiple = ChatPromptTemplate.from_template(template_multiple)
# prompt = prompt_multiple.invoke({"adjective":"funny", "animal":"cat"})
# print("\n--- Prompt from Multiple Template ----")
# print(prompt)

# ChatPromptTemplate es una clase que facilita la creación de prompts 
# para modelos de chat. Permite definir una plantilla de texto con placeholders 
# que pueden ser reemplazados con valores específicos cuando se invoca 
# la plantilla.


# # PART 3: Create a ChatPromptTemplate using a template file
# template_file = "prompt_templates/chat_template_1.txt"
# prompt_template = ChatPromptTemplate.from_file(template_file)
# prompt = prompt_template.invoke({"animal": "dog", "adjective": "funny"})
# print("\n--- Prompt from File ----")
# print(prompt)

# Parte 3: Prompt with System and Human Messages(Using Tuples)
# messages = [
#     ("system","You are a comedian who tells jokes about {topic}"),
#     ("human","Tellm me a {joke_acount} jokes")
# ]

prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic":"dog", "joke_acount":"two"})
print("\n--- Prompt with System and Human Messages (Tuple) ----")
print(prompt)

# Extra information about Part 3
messages = [
    ("system","You are a comedian who tells jokes about {topic}"),
    HumanMessage(content ="Tell me 3 jokes")
]

# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic":"dog"})
# print("\n--- Prompt with System and Human Messages (Tuple) ----")
# print(prompt)


# NOT FOUND 
# messages = [
#     ("system", "You are a comedian who tells jokes about {topic}."),
#     HumanMessage(content="Tell me {joke_count} jokes."),
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
# print("\n----- Prompt with System and Human Messages (Tuple) -----\n")
# print(prompt)