# MCP Sampling - Código Explicado por Partes

## Parte 1: Imports y Configuración Inicial

### 📦 Imports del Cliente
```python
import asyncio
import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)
```

**📝 Notas:**
- `asyncio`: Para programación asíncrona
- `dotenv`: Para cargar variables de entorno desde `.env`
- `AsyncAnthropic`: Cliente oficial de Claude
- `mcp.*`: Tipos y clases del protocolo MCP
- **Concepto clave**: MCP separa tipos de datos de funcionalidad

### 🔧 Configuración de Variables
```python
# Load environment variables from .env file
load_dotenv()

anthropic_client = AsyncAnthropic()
model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
```

**📝 Notas:**
- `load_dotenv()`: Carga `.env` en variables de entorno
- `AsyncAnthropic()`: Toma automáticamente `ANTHROPIC_API_KEY` del entorno
- **Por qué funciona**: El cliente de Anthropic busca la API key en variables de entorno

### 🚀 Configuración del Servidor
```python
server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)
```

**📝 Notas:**
- `StdioServerParameters`: Le dice al cliente cómo lanzar el servidor
- `command="uv"`: Usa UV para ejecutar
- `args=["run", "server.py"]`: Equivale a `uv run server.py`
- **Importante**: El cliente controla el ciclo de vida del servidor

---

## Parte 2: Función Chat - Ejecutor de Claude

### 🎯 Conversión de Mensajes MCP a Anthropic
```python
async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
```

**📝 Notas:**
- **Input**: `SamplingMessage` (formato MCP)
- **Output**: `dict` (formato Anthropic)
- `hasattr(msg.content, "text")`: Verificación de seguridad
- **Por qué convertir**: MCP y Anthropic usan formatos diferentes

### 🤖 Llamada Real a Claude
```python
    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text
```

**📝 Notas:**
- **AQUÍ** es donde realmente se ejecuta Claude
- `response.content`: Lista de partes de la respuesta
- `"".join([...])`: Concatena todas las partes de texto
- **Importante**: Esta función NO sabe nada de MCP, solo Claude

---

## Parte 3: Sampling Callback - El Corazón del Sistema

### 🔄 Definición del Handler
```python
async def sampling_callback(
    context: RequestContext, 
    params: CreateMessageRequestParams
):
```

**📝 Notas:**
- **Función más importante** del sistema MCP Sampling
- `context`: Información sobre la solicitud MCP
- `params`: Contiene los mensajes que envió el servidor
- **Se ejecuta automáticamente** cuando el servidor pide sampling

### 🎬 Ejecución y Respuesta
```python
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )
```

**📝 Notas:**
- `params.messages`: Los `SamplingMessage` que envió el servidor
- `await chat(...)`: Ejecuta Claude con esos mensajes
- `CreateMessageResult`: Formato estándar MCP para respuestas
- **Flujo**: MCP → Claude → MCP

---

## Parte 4: Función Principal - El Orquestador

### 🚀 Inicio de Comunicación
```python
async def run():
    async with stdio_client(server_params) as (read, write):
```

**📝 Notas:**
- `stdio_client()`: Lanza el servidor y establece comunicación
- `(read, write)`: Canales de comunicación stdin/stdout
- **async with**: Garantiza que el servidor se cierre correctamente

### 📝 Registro del Callback
```python
        async with ClientSession(
            read, write, 
            sampling_callback=sampling_callback
        ) as session:
```

**📝 Notas:**
- **MOMENTO CLAVE**: Aquí se registra el handler de sampling
- `sampling_callback=sampling_callback`: "Cuando haya sampling, ejecuta esta función"
- Sin esto, las solicitudes de sampling fallarían

### 🔧 Inicialización y Handshake
```python
            await session.initialize()
```

**📝 Notas:**
- Handshake MCP entre cliente y servidor
- Intercambian capacidades y configuración
- **Necesario** antes de usar herramientas

### 🛠️ Llamada a Herramienta
```python
            result = await session.call_tool(
                name="summarize",
                arguments={"text_to_summarize": "lots of text"},
            )
            print(result.content)
```

**📝 Notas:**
- `call_tool()`: Invoca una herramienta del servidor
- `name="summarize"`: Debe coincidir con `@mcp.tool()` del servidor
- `arguments`: Parámetros que recibe la función del servidor
- **Aquí comienza** la cadena de sampling

---

## Parte 5: Servidor - La Lógica de Herramientas

### 📦 Imports del Servidor
```python
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")
```

**📝 Notas:**
- `FastMCP`: Framework simplificado para servidores MCP
- `Context`: Contiene la sesión para comunicarse con el cliente
- **Diferencia**: El servidor NO importa `anthropic`

### 🛠️ Definición de Herramienta
```python
@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
```

**📝 Notas:**
- `@mcp.tool()`: Registra la función como herramienta MCP
- `ctx: Context`: **CRUCIAL** para hacer sampling
- El nombre de la función (`summarize`) es el nombre de la herramienta

### 📝 Preparación del Prompt
```python
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """
```

**📝 Notas:**
- Construcción del prompt que se enviará al cliente
- `text_to_summarize`: Viene de `arguments` del cliente
- **El servidor prepara** lo que quiere preguntar a la IA

### 🔄 Solicitud de Sampling
```python
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user", 
                content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )
```

**📝 Notas:**
- **MOMENTO CLAVE**: `ctx.session.create_message()` NO ejecuta Claude
- Envía una solicitud de sampling al cliente
- `SamplingMessage`: Formato MCP para mensajes
- **El cliente recibirá esto** en `sampling_callback()`

### ✅ Retorno del Resultado
```python
    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")
```

**📝 Notas:**
- `result`: El `CreateMessageResult` que devolvió el cliente
- `result.content.text`: La respuesta real de Claude
- **El servidor devuelve** esto como resultado de la herramienta

---

## Parte 6: Entry Point
```python
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
```

**📝 Notas:**
- Punto de entrada estándar de Python
- `asyncio.run()`: Ejecuta la función asíncrona principal
- **Inicia todo el proceso** de sampling

---

## 🔄 Flujo Completo con Referencias de Código

1. **Cliente inicia** → `asyncio.run(run())`
2. **Lanza servidor** → `stdio_client(server_params)`
3. **Registra callback** → `ClientSession(sampling_callback=sampling_callback)`
4. **Llama herramienta** → `session.call_tool("summarize", ...)`
5. **Servidor ejecuta** → `@mcp.tool() async def summarize(...)`
6. **Solicita sampling** → `ctx.session.create_message(...)`
7. **Cliente maneja** → `sampling_callback(context, params)`
8. **Ejecuta Claude** → `await chat(params.messages)`
9. **Devuelve resultado** → `CreateMessageResult(...)`
10. **Servidor termina** → `return result.content.text`
11. **Cliente imprime** → `print(result.content)`

---

## 📚 Conceptos para Recordar

### ¿Qué es CreateMessageResult?
```python
CreateMessageResult(
    role="assistant",          # Quien responde (siempre "assistant" para IA)
    model=model,              # Qué modelo se usó
    content=TextContent(      # El contenido de la respuesta
        type="text", 
        text=text             # La respuesta real de Claude
    ),
)
```

### ¿Por qué sampling_callback?
- Es el **puente** entre MCP y Claude
- Se registra una vez, se ejecuta muchas veces
- **Sin él**, el servidor no puede usar IA

### ¿Por qué el servidor no llama Claude directamente?
- **Separación de responsabilidades**: Servidor = lógica, Cliente = IA
- **Seguridad**: API keys en el cliente
- **Flexibilidad**: Diferentes clientes pueden usar diferentes modelos
