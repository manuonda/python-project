# LangChain Prompt Template

## Introducción

LangChain es una biblioteca poderosa para la creación de aplicaciones de procesamiento de lenguaje natural (NLP). Un componente clave de LangChain es el uso de plantillas de prompts (prompt templates) que permiten generar prompts dinámicos y reutilizables para modelos de lenguaje.

## ¿Qué es un Prompt Template?

Un prompt template es una plantilla que define la estructura de un prompt que se enviará a un modelo de lenguaje. Los prompt templates permiten insertar variables dinámicas en el prompt, lo que facilita la generación de prompts personalizados basados en diferentes contextos o datos de entrada.

## Ejemplo de Uso

A continuación se muestra un ejemplo básico de cómo crear y utilizar un prompt template en LangChain:

```python
from langchain.prompts import PromptTemplate

# Definir el template con variables
template = "Hola, mi nombre es {nombre} y soy {profesion}."

# Crear una instancia de PromptTemplate
prompt = PromptTemplate(template)

# Generar un prompt con valores específicos
prompt_text = prompt.generate(nombre="Manuel", profesion="desarrollador")
print(prompt_text)
```

## Beneficios de Usar Prompt Templates

- **Reutilización**: Los prompt templates permiten reutilizar la misma estructura de prompt con diferentes datos de entrada.
- **Mantenimiento**: Facilitan el mantenimiento del código, ya que los cambios en la estructura del prompt se pueden realizar en un solo lugar.
- **Flexibilidad**: Permiten generar prompts dinámicos y personalizados según el contexto o los datos de entrada.

## Conclusión

Los prompt templates en LangChain son una herramienta esencial para la creación de aplicaciones NLP eficientes y flexibles. Al utilizar prompt templates, los desarrolladores pueden generar prompts personalizados de manera sencilla y mantener un código limpio y reutilizable.
## Ejemplos Avanzados

### Ejemplo 1: Uso de ChatPromptTemplate con un Modelo de Chat

En este ejemplo, se muestra cómo crear un `ChatPromptTemplate` utilizando una cadena de plantilla y un modelo de chat:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Cargar variables de entorno
load_dotenv()

# Crear el modelo de chat
model = ChatOpenAI(model="gpt-4o")

# Definir el template con una variable
template = "Cuéntame un chiste sobre {tema}"
prompt_template = ChatPromptTemplate.from_template(template)

# Generar el prompt con un valor específico
prompt = prompt_template.invoke({"tema": "gatos"})
resultado = model.invoke(prompt)
print(resultado.content)
```

### Ejemplo 2: Prompt con Múltiples Marcadores de Posición

Este ejemplo muestra cómo crear un `ChatPromptTemplate` con múltiples marcadores de posición:

```python
# Definir el template con múltiples variables
template_multiple = """Eres un asistente útil
Humano: Cuéntame una historia {adjetivo} sobre un {animal}
Asistente:"""
prompt_template = ChatPromptTemplate.from_template(template_multiple)

# Generar el prompt con valores específicos
prompt = prompt_template.invoke({"adjetivo": "divertida", "animal": "panda"})
resultado = model.invoke(prompt)
print(resultado.content)
```

### Ejemplo 3: Prompt con Mensajes del Sistema y del Usuario

En este ejemplo, se utiliza un `ChatPromptTemplate` con mensajes del sistema y del usuario:

```python
# Definir los mensajes del sistema y del usuario
mensajes = [
    ("system", "Eres un comediante que cuenta chistes sobre {tema}"),
    ("human", "Cuéntame {cantidad_chistes} chistes")
]
prompt_template = ChatPromptTemplate.from_messages(mensajes)

# Generar el prompt con valores específicos
prompt = prompt_template.invoke({"tema": "abogados", "cantidad_chistes": 3})
resultado = model.invoke(prompt)
print(resultado.content)
```

Estos ejemplos muestran cómo utilizar `ChatPromptTemplate` en diferentes escenarios para generar prompts dinámicos y personalizados con LangChain.