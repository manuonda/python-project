##|11
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Herramientas mejoradas
@tool
def multiply(a: float, b: float) -> str:
    """Multiplica dos números"""
    result = a * b
    return f"El resultado de {a} × {b} = {result}"

@tool
def sum_numbers(a: float, b: float) -> str:
    """Suma dos números"""
    result = a + b
    return f"El resultado de {a} + {b} = {result}"

@tool
def web_search(query: str) -> str:
    """Realiza una búsqueda web simulada"""
    simulated_results = {
        "langgraph": "LangGraph es un framework para crear agentes con grafos de estado...",
        "python": "Python es un lenguaje de programación interpretado...",
        "ai": "La inteligencia artificial es la simulación de procesos de inteligencia humana..."
    }
    for key in simulated_results:
        if key in query.lower():
            return f"Resultados para '{query}': {simulated_results[key]}"
    return f"Resultados generales para '{query}': Información encontrada en la web."

@tool
def calculator(expression: str) -> str:
    """Evalúa expresiones matemáticas complejas"""
    try:
        result = eval(expression)
        return f"Resultado de '{expression}' = {result}"
    except Exception as e:
        return f"Error al evaluar: {str(e)}"

TOOLS = [multiply, sum_numbers, web_search, calculator]

# LLM configurado
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent_llm = llm.bind_tools(TOOLS, parallel_tool_calls=False)

# Router inteligente
def route_by_task(state: MessagesState) -> Literal["math_specialist", "research_specialist", "general", "end"]:
    """Enruta según el tipo de tarea detectada"""
    last_message = state["messages"][-1].content.lower()
    
    # Detectar matemáticas
    math_keywords = ["multiplica", "suma", "calcula", "resultado", "operación", "×", "+", "-", "*"]
    if any(keyword in last_message for keyword in math_keywords):
        return "math_specialist"
    
    # Detectar investigación
    research_keywords = ["busca", "investiga", "información", "qué es", "explica", "search"]
    if any(keyword in last_message for keyword in research_keywords):
        return "research_specialist"
    
    # Verificar si hay tool_calls pendientes
    last_ai_message = next((msg for msg in reversed(state["messages"]) if hasattr(msg, 'tool_calls')), None)
    if last_ai_message and getattr(last_ai_message, 'tool_calls', []):
        return "general"
    
    return "end"

# Especialistas
def math_specialist(state: MessagesState):
    """Especialista en matemáticas y cálculos"""
    system_msg = SystemMessage(content="""Eres un matemático experto. 
    - Analiza el problema paso a paso
    - Usa las herramientas disponibles (multiply, sum_numbers, calculator)
    - Explica tu razonamiento antes de calcular
    - Verifica los resultados
    """)
    response = agent_llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

def research_specialist(state: MessagesState):
    """Especialista en investigación y búsquedas"""
    system_msg = SystemMessage(content="""Eres un investigador experto.
    - Usa web_search para encontrar información
    - Resume los hallazgos de forma clara y concisa
    - Cita las fuentes cuando sea relevante
    - Proporciona contexto útil
    """)
    response = agent_llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

def general_assistant(state: MessagesState):
    """Asistente general para otras consultas"""
    system_msg = SystemMessage(content="""Eres un asistente útil y versátil.
    - Responde de forma clara y directa
    - Usa herramientas cuando sea necesario
    - Mantén un tono amigable y profesional
    """)
    response = agent_llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

# Construcción del grafo
graph = StateGraph(MessagesState)

# Agregar nodos
graph.add_node("router", lambda state: {"messages": state["messages"]})
graph.add_node("math_specialist", math_specialist)
graph.add_node("research_specialist", research_specialist)
graph.add_node("general", general_assistant)
graph.add_node("tools", ToolNode(TOOLS))

# Configurar edges
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    route_by_task,
    {
        "math_specialist": "math_specialist",
        "research_specialist": "research_specialist",
        "general": "general",
        "end": "__end__"
    }
)

# Cada especialista puede llamar herramientas
graph.add_conditional_edges("math_specialist", tools_condition)
graph.add_conditional_edges("research_specialist", tools_condition)
graph.add_conditional_edges("general", tools_condition)

# Después de usar tools, volver al router
graph.add_edge("tools", "router")

# Compilar
advanced_router_agent = graph.compile()

# Pruebas
if __name__ == "__main__":
    print("=== Ejemplo 1: Tarea matemática ===")
    result1 = advanced_router_agent.invoke({
        "messages": [HumanMessage(content="Multiplica 25 por 8 y luego suma 100 al resultado")]
    })
    for msg in result1["messages"]:
        msg.pretty_print()
    
    print("\n=== Ejemplo 2: Tarea de investigación ===")
    result2 = advanced_router_agent.invoke({
        "messages": [HumanMessage(content="Busca información sobre LangGraph y explícame qué es")]
    })
    for msg in result2["messages"]:
        msg.pretty_print()
        
        
        
2. React Agent con Memoria Conversacional

from typing import Dict, Any
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Estado con memoria
class MemoryState(TypedDict):
    messages: list
    user_data: Dict[str, Any]  # Información del usuario
    conversation_context: Dict[str, Any]  # Contexto de la conversación
    calculations_history: list  # Historial de cálculos

# Herramientas con memoria
@tool
def save_preference(key: str, value: str) -> str:
    """Guarda una preferencia del usuario"""
    return f"✓ Guardada preferencia: {key} = {value}"

@tool
def recall_preference(key: str) -> str:
    """Recupera una preferencia guardada"""
    return f"Recuperando preferencia: {key}"

@tool
def save_calculation(expression: str, result: str) -> str:
    """Guarda un cálculo en el historial"""
    return f"✓ Cálculo guardado: {expression} = {result}"

@tool
def multiply(a: float, b: float) -> str:
    """Multiplica dos números"""
    return f"{a * b}"

MEMORY_TOOLS = [save_preference, recall_preference, save_calculation, multiply]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
memory_llm = llm.bind_tools(MEMORY_TOOLS, parallel_tool_calls=False)

def memory_assistant(state: MemoryState):
    """Asistente con memoria contextual"""
    # Construir contexto desde la memoria
    context_parts = []
    
    if state["user_data"]:
        prefs = ", ".join(f"{k}: {v}" for k, v in state["user_data"].items())
        context_parts.append(f"Preferencias del usuario: {prefs}")
    
    if state["calculations_history"]:
        last_calcs = state["calculations_history"][-3:]  # Últimos 3 cálculos
        calcs = "; ".join(last_calcs)
        context_parts.append(f"Cálculos recientes: {calcs}")
    
    if state["conversation_context"]:
        ctx = ", ".join(f"{k}: {v}" for k, v in state["conversation_context"].items())
        context_parts.append(f"Contexto: {ctx}")
    
    memory_context = "\n".join(context_parts) if context_parts else "Sin información previa"
    
    system_msg = SystemMessage(content=f"""Eres un asistente con memoria contextual.

MEMORIA DISPONIBLE:
{memory_context}

CAPACIDADES:
- Recordar preferencias del usuario (usa save_preference)
- Recuperar información guardada (usa recall_preference)
- Guardar cálculos importantes (usa save_calculation)
- Realizar operaciones matemáticas

Usa la memoria activamente y menciona información relevante del contexto.
""")
    
    response = memory_llm.invoke([system_msg] + state["messages"])
    
    # Actualizar estado basado en la respuesta
    new_user_data = dict(state["user_data"])
    new_calcs = list(state["calculations_history"])
    new_context = dict(state["conversation_context"])
    
    # Parsear acciones de memoria (simplificado)
    if hasattr(response, 'content') and response.content:
        content = response.content
        if "preferencia:" in content.lower() and "=" in content:
            # Extraer preferencia guardada
            try:
                parts = content.split("preferencia:")[1].split("=")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].split()[0].strip()
                    new_user_data[key] = value
            except:
                pass
    
    return {
        "messages": [response],
        "user_data": new_user_data,
        "calculations_history": new_calcs,
        "conversation_context": new_context
    }

# Construir grafo
memory_graph = StateGraph(MemoryState)
memory_graph.add_node("assistant", memory_assistant)
memory_graph.add_node("tools", ToolNode(MEMORY_TOOLS))

memory_graph.add_edge(START, "assistant")
memory_graph.add_conditional_edges("assistant", tools_condition)
memory_graph.add_edge("tools", "assistant")

memory_agent = memory_graph.compile()

# Conversación con memoria
if __name__ == "__main__":
    # Estado inicial
    current_state = {
        "messages": [],
        "user_data": {},
        "conversation_context": {},
        "calculations_history": []
    }
    
    # Turno 1
    print("=== Turno 1: Guardar preferencia ===")
    current_state["messages"].append(HumanMessage(content="Mi nombre es Manuel y mi color favorito es azul"))
    result = memory_agent.invoke(current_state)
    result["messages"][-1].pretty_print()
    current_state = result
    
    # Turno 2
    print("\n=== Turno 2: Cálculo ===")
    current_state["messages"].append(HumanMessage(content="Multiplica 15 por 8"))
    result = memory_agent.invoke(current_state)
    result["messages"][-1].pretty_print()
    current_state = result
    
    # Turno 3
    print("\n=== Turno 3: Recordar contexto ===")
    current_state["messages"].append(HumanMessage(content="¿Recuerdas mi color favorito y el último cálculo?"))
    result = memory_agent.invoke(current_state)
    result["messages"][-1].pretty_print()
    
    print("\n=== Estado final de memoria ===")
    print(f"User data: {result['user_data']}")
    print(f"Calculations: {result['calculations_history']}")
    
    ##3. React Agent Conversacional Multi-turno

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Herramientas interactivas
@tool
def get_user_info(info_type: str) -> str:
    """Solicita información al usuario"""
    return f"Necesito que me proporciones: {info_type}"

@tool
def process_data(data: str, operation: str) -> str:
    """Procesa datos según la operación solicitada"""
    return f"Procesando '{data}' con operación '{operation}'"

@tool
def calculate(expression: str) -> str:
    """Calcula una expresión matemática"""
    try:
        result = eval(expression)
        return f"Resultado: {result}"
    except:
        return "Error en el cálculo"

INTERACTIVE_TOOLS = [get_user_info, process_data, calculate]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
interactive_llm = llm.bind_tools(INTERACTIVE_TOOLS)

def interactive_assistant(state: MessagesState):
    """Asistente que mantiene contexto conversacional"""
    # Contar mensajes para entender el flujo
    num_interactions = len([m for m in state["messages"] if isinstance(m, HumanMessage)])
    
    system_msg = SystemMessage(content=f"""Eres un asistente conversacional interactivo.

TURNO DE CONVERSACIÓN: {num_interactions}

INSTRUCCIONES:
- Mantén el contexto de la conversación completa
- Recuerda información de mensajes anteriores
- Haz preguntas de seguimiento cuando sea necesario
- Confirma acciones antes de ejecutarlas
- Sé proactivo sugiriendo próximos pasos

Analiza TODO el historial de mensajes antes de responder.
""")
    
    response = interactive_llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

# Grafo conversacional
interactive_graph = StateGraph(MessagesState)
interactive_graph.add_node("assistant", interactive_assistant)
interactive_graph.add_node("tools", ToolNode(INTERACTIVE_TOOLS))

interactive_graph.add_edge(START, "assistant")
interactive_graph.add_conditional_edges("assistant", tools_condition)
interactive_graph.add_edge("tools", "assistant")

conversational_agent = interactive_graph.compile()

# Simulación de conversación multi-turno
if __name__ == "__main__":
    conversation_state = {"messages": []}
    
    user_inputs = [
        "Hola, necesito ayuda con unos cálculos",
        "Quiero calcular el área de un círculo con radio 5",
        "Perfecto, ahora calcula el volumen de una esfera con el mismo radio",
        "Gracias, ¿puedes compararlos?"
    ]
    
    for i, user_input in enumerate(user_inputs, 1):
        print(f"\n{'='*60}")
        print(f"TURNO {i}: Usuario")
        print(f"{'='*60}")
        print(f"👤 {user_input}")
        
        conversation_state["messages"].append(HumanMessage(content=user_input))
        result = conversational_agent.invoke(conversation_state)
        
        print(f"\n🤖 Asistente:")
        result["messages"][-1].pretty_print()
        
        conversation_state = result
    
    print(f"\n{'='*60}")
    print(f"RESUMEN: {len(conversation_state['messages'])} mensajes en total")
    print(f"{'='*60}")
    
    
    Router avanzado: Especialistas por dominio (matemáticas, investigación)
Memoria: Estado persistente entre turnos con user_data y calculations_history
Multi-turno: Conversaciones naturales manteniendo contexto completo