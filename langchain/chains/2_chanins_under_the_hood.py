from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda, RunnableSequence

# load_dotenv
load_dotenv()

#create model 
model = ChatOpenAI(model="gpt-4o")

# Define prompt templates 
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a comedian who tells jokes about {topic}."),
        ("human", "Tell me {joke_count} jokes."),
    ]
)

# Create individual runnables (steps in the chain)

# Formatear el prompt usando los datos de entrada
format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))

# Invocar el modelo con el prompt formateado 
invoke_model = RunnableLambda(lambda  x:model.invoke(x.to_messages()))

# Parsear la salida del modelo para obtener el contenido
parse_output = RunnableLambda(lambda x: x.content)

# Secuencia de cadnea 
chain = RunnableSequence(first = format_prompt, middle=[invoke_model], last=parse_output)

#Execute chain 
response = chain.invoke({"topic":"lawyers","joke_count":3})

#salida 
print(response)
