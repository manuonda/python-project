# MCP Sampling - Guía Completa

## ¿Qué es MCP Sampling?

**MCP Sampling** es un patrón del protocolo Model Context Protocol donde:

- El **servidor** define herramientas/funciones
- El **cliente** maneja las llamadas a modelos de IA (como Claude, GPT, etc.)
- Cuando el servidor necesita IA, hace una **solicitud de sampling** al cliente
- El cliente ejecuta la IA y devuelve el resultado

### Analogía Simple
Imagina que eres un **chef** (servidor) que sabe hacer recetas, pero no tienes ingredientes. Tu **asistente** (cliente) tiene todos los ingredientes (acceso a la IA). Cuando necesitas un ingrediente, le pides a tu asistente que te lo traiga.

## Componentes del Proyecto

### 1. Server.py - El "Chef" (Servidor MCP)

```python
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")

@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    """
    Herramienta que resume texto.
    ¡IMPORTANTE! No llama directamente a Claude.
    """
    
    # 1. Prepara el prompt
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    # 2. 🎯 SOLICITUD DE SAMPLING
    # ctx.session.create_message() NO llama a Claude directamente
    # Envía una solicitud al cliente: "Oye, ejecuta esto en tu IA"
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

    # 3. El cliente ejecutará Claude y devolverá el resultado aquí
    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")
```

**Puntos Clave del Servidor:**
- ✅ Define herramientas con `@mcp.tool()`
- ✅ **NO** tiene acceso directo a Claude
- ✅ Usa `ctx.session.create_message()` para solicitar sampling
- ✅ El cliente se encarga de la ejecución real de IA

### 2. Client.py - El "Asistente" (Cliente MCP)

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

# 🔧 Configuración
load_dotenv()
anthropic_client = AsyncAnthropic()  # Cliente real de Claude
model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

# 🚀 Configuración del servidor a lanzar
server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)
```

#### Función Chat - Ejecutor Real de Claude

```python
async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    """
    Convierte mensajes MCP a formato Anthropic y ejecuta Claude
    """
    messages = []
    
    # Convierte SamplingMessage a formato Anthropic
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    # 🎯 LLAMADA REAL A CLAUDE
    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    # Extrae solo el texto de la respuesta
    text = "".join([p.text for p in response.content if p.type == "text"])
    return text
```

#### Sampling Callback - El "Handler" de Solicitudes

```python
async def sampling_callback(
    context: RequestContext, 
    params: CreateMessageRequestParams
):
    """
    🚨 FUNCIÓN CLAVE DEL SAMPLING
    
    Se ejecuta automáticamente cuando el servidor hace:
    ctx.session.create_message()
    
    Args:
        context: Contexto de la solicitud MCP
        params: Parámetros enviados por el servidor
                params.messages contiene los SamplingMessage del servidor
    
    Returns:
        CreateMessageResult: Respuesta formateada para MCP
    """
    
    # 1. Ejecuta Claude con los mensajes del servidor
    text = await chat(params.messages)

    # 2. Devuelve resultado en formato MCP
    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )
```

#### Función Principal - Orquestador

```python
async def run():
    """
    Función principal que orquesta todo el flujo
    """
    
    # 1. 🚀 Inicia comunicación con el servidor
    async with stdio_client(server_params) as (read, write):
        
        # 2. 📝 Registra el sampling callback
        async with ClientSession(
            read, write, 
            sampling_callback=sampling_callback  # ⭐ REGISTRO DEL HANDLER
        ) as session:
            
            # 3. Inicializa la sesión MCP
            await session.initialize()

            # 4. 🎯 LLAMA A LA HERRAMIENTA DEL SERVIDOR
            result = await session.call_tool(
                name="summarize",  # Nombre de la herramienta en server.py
                arguments={"text_to_summarize": "lots of text"},
            )
            
            # 5. Imprime el resultado final
            print(result.content)
```

## Flujo Completo Paso a Paso

```
📱 CLIENTE                    🖥️  SERVIDOR

1. Inicia servidor ─────────→ server.py arranca
2. Registra callback        
3. session.call_tool() ─────→ 4. @mcp.tool() summarize()
                               5. ctx.session.create_message()
6. sampling_callback() ←──────    (solicitud de sampling)
7. chat() ejecuta Claude      
8. return CreateMessageResult ──→ 9. Recibe respuesta
                               10. return result
11. print(result.content) ←────    
```

### Flujo Detallado

1. **Cliente inicia:** `uv run client.py`
2. **Cliente lanza servidor:** Ejecuta `uv run server.py`
3. **Registro de callback:** `ClientSession(sampling_callback=sampling_callback)`
4. **Llamada a herramienta:** `session.call_tool("summarize", {...})`
5. **Servidor recibe:** Función `summarize()` se ejecuta
6. **Solicitud de sampling:** `ctx.session.create_message()`
7. **Cliente maneja sampling:** Se ejecuta `sampling_callback()`
8. **Ejecución de Claude:** Función `chat()` llama a Anthropic API
9. **Respuesta al servidor:** `CreateMessageResult` regresa al servidor
10. **Servidor termina:** Devuelve resultado de la herramienta
11. **Cliente imprime:** `print(result.content)`

## Conceptos Clave

### ¿Qué es "Sampling"?
En el contexto de MCP, **sampling** es el proceso de:
- Enviar mensajes a un modelo de IA
- Recibir respuestas generadas
- Es llamado "sampling" porque los modelos "muestrean" de su distribución de probabilidades

### CreateMessageResult
```python
CreateMessageResult(
    role="assistant",           # Quien responde
    model=model,               # Qué modelo se usó
    content=TextContent(       # El contenido de la respuesta
        type="text", 
        text=text
    ),
)
```

### SamplingMessage
```python
SamplingMessage(
    role="user",               # Quien envía el mensaje
    content=TextContent(       # El contenido del mensaje
        type="text", 
        text=prompt
    )
)
```

## Ventajas del Patrón MCP Sampling

1. **🔐 Seguridad**: Las API keys permanecen en el cliente
2. **🔄 Reutilización**: Un servidor puede usarse con diferentes clientes/modelos
3. **🎯 Separación**: Servidor = lógica de herramientas, Cliente = acceso a IA
4. **⚡ Flexibilidad**: Cada cliente puede usar diferentes modelos (Claude, GPT, etc.)

## Comandos para Ejecutar

```bash
# Instalar dependencias
uv sync

# Ejecutar el cliente (que automáticamente lanza el servidor)
uv run client.py
```

## Variables de Entorno Requeridas

Crear archivo `.env`:
```properties
CLAUDE_MODEL="claude-3-5-sonnet-20241022"
ANTHROPIC_API_KEY="tu-api-key-aqui"
USE_UV=1
```

## Posibles Extensiones

- **Múltiples herramientas**: Agregar más `@mcp.tool()` en el servidor
- **Diferentes modelos**: Cambiar el modelo en el cliente
- **Sistema de prompts**: Prompts más sofisticados
- **Manejo de errores**: Agregar try/catch en sampling_callback
- **Logging**: Agregar logs para debugging

---

**💡 Recuerda:** El servidor define QUÉ hacer, el cliente define CÓMO ejecutar la IA.
