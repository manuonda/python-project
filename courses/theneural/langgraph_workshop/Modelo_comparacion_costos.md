# 📊 COMPARACIÓN DE COSTOS DE MODELOS AI (Actualizado Octubre 2025)

## 💰 COSTOS POR 1K TOKENS 

### OpenAI Models
```python
MODEL_COSTS = {
    "gpt-4o": {
        "input": 0.0025,   # $2.50 por 1M tokens = $0.0025 por 1K ✅ Confirmado
        "output": 0.01,    # $10.00 por 1M tokens = $0.01 por 1K ✅ Confirmado
        "cached_input": 0.00125,  # 50% descuento con cache
        "vision": "Incluido en tokens estándar",  # ~700 tokens por imagen 1024x1024
        "quality": "Excelente",
        "speed": "Rápido (77.4 tokens/segundo)",
        "context": "128K tokens",
        "max_output": "16.4K tokens"
    },
    "gpt-4o-mini": {
        "input": 0.00015,  # $0.15 por 1M tokens ✅ Confirmado
        "output": 0.0006,  # $0.60 por 1M tokens ✅ Confirmado
        "cached_input": 0.000075,  # 50% descuento con cache
        "vision": "Incluido en tokens estándar",
        "quality": "Muy bueno (82% MMLU)",
        "speed": "Muy rápido",
        "context": "128K tokens",
        "max_output": "16K tokens"
    },
    
    # 🆕 NUEVOS MODELOS GEMINI 2.5
    "gemini-2.5-pro": {
        "input": 0.00125,  # $1.25 por 1M tokens (≤200K contexto)
        "input_large": 0.0025,  # $2.50 por 1M tokens (>200K contexto)
        "output": 0.01,    # $10.00 por 1M tokens (≤200K contexto)
        "output_large": 0.015,  # $15.00 por 1M tokens (>200K contexto)
        "vision": "Incluido",  # Sin costo adicional
        "audio": 0.001,    # $1.00 por 1M tokens audio
        "cache": 0.000125,  # Cache muy económico
        "quality": "Excelente - Modelo frontier",
        "speed": "Rápido",
        "context": "2M tokens",
        "batch_discount": "50%"  # Descuento para procesamiento batch
    },
    "gemini-2.5-flash": {
        "input": 0.0003,   # $0.30 por 1M tokens texto/imagen/video
        "output": 0.0025,  # $2.50 por 1M tokens
        "audio_input": 0.001,  # $1.00 por 1M tokens audio
        "vision": "Incluido",
        "cache": 0.00003,  # Cache ultra económico
        "quality": "Muy bueno - Modelo de razonamiento híbrido",
        "speed": "Muy rápido",
        "context": "1M tokens",
        "batch_discount": "50%"
    },
    "gemini-2.5-flash-lite": {
        "input": 0.0001,   # $0.10 por 1M tokens ⚡ MÁS BARATO
        "output": 0.0004,  # $0.40 por 1M tokens
        "audio_input": 0.0003,  # $0.30 por 1M tokens audio
        "vision": "Incluido",
        "cache": 0.000025,
        "quality": "Bueno - Optimizado para escala",
        "speed": "Ultra rápido",
        "context": "Contexto moderado",
        "batch_discount": "50%"
    },
    
    # 🆕 GEMINI 2.0 (Versión anterior pero aún disponible)
    "gemini-2.0-flash": {
        "input": 0.0001,   # $0.10 por 1M tokens
        "output": 0.0004,  # $0.40 por 1M tokens
        "audio_input": 0.0007,  # $0.70 por 1M tokens audio
        "vision": "Incluido",
        "cache": 0.000025,
        "quality": "Bueno - Era de agentes",
        "speed": "Muy rápido",
        "context": "1M tokens",
        "batch_discount": "50%"
    }
}
```

## 🎯 ESTRATEGIA INTELIGENTE DE SELECCIÓN

### Por Tipo de Documento
```python
DOCUMENT_STRATEGIES = {
    "factura_simple": {
        "primary": "gemini-2.5-flash-lite",  # $0.0001 entrada - MÁS BARATO
        "secondary": "gpt-4o-mini",          # $0.00015 entrada - Backup confiable
        "fallback": "gemini-2.5-flash"       # $0.0003 entrada - Si necesitas más poder
    },
    "factura_compleja": {
        "primary": "gpt-4o",                 # $0.0025 - Mejor calidad OCR
        "secondary": "gemini-2.5-pro",       # $0.00125 - Excelente alternativa
        "budget": "gemini-2.5-flash"         # $0.0003 - Opción económica potente
    },
    "recibo_simple": {
        "primary": "gemini-2.5-flash-lite",  # $0.0001 - Ultra económico
        "fallback": "gemini-2.0-flash"       # $0.0001 - Igual de barato
    },
    "documento_dañado": {
        "primary": "gpt-4o",                 # Mejor para documentos difíciles
        "fallback": "gemini-2.5-pro"         # Excelente procesamiento visual
    },
    "procesamiento_masivo": {
        "primary": "gemini-2.5-flash-lite",  # Con Batch API: $0.00005 entrada
        "batch_mode": True,                  # 50% descuento adicional
        "estimated_cost": "$0.05 por 1000 documentos"
    }
}
```

## 📈 ANÁLISIS COMPARATIVO DE COSTOS

### Procesamiento de 1,000 Facturas Simples (500 tokens promedio c/u)
```python
COST_COMPARISON = {
    "gemini-2.5-flash-lite": {
        "standard": 0.05,     # $0.05 USD
        "batch": 0.025,       # $0.025 USD con Batch API
        "savings": "95% vs GPT-4o"
    },
    "gpt-4o-mini": {
        "standard": 0.075,    # $0.075 USD
        "cached": 0.0375,     # Con cache
        "savings": "85% vs GPT-4o"
    },
    "gemini-2.5-flash": {
        "standard": 0.15,     # $0.15 USD
        "batch": 0.075,       # Con Batch API
        "savings": "70% vs GPT-4o"
    },
    "gpt-4o": {
        "standard": 1.25,     # $1.25 USD
        "cached": 0.625,      # Con cache
        "baseline": "100%"
    }
}
```

## 🚀 OPTIMIZACIONES RECOMENDADAS

### 1. **Para Volumen Alto (>10,000 docs/mes)**
```python
{
    "modelo_primario": "gemini-2.5-flash-lite",
    "usar_batch_api": True,  # 50% descuento adicional
    "costo_estimado": "$0.00005 por 1K tokens entrada",
    "ahorro_mensual": "~95% vs modelos premium"
}
```

### 2. **Para Calidad Premium**
```python
{
    "modelo_primario": "gemini-2.5-pro",
    "ventajas": [
        "2M tokens de contexto",
        "Mejor precio que GPT-4o ($1.25 vs $2.50)",
        "Audio y visión incluidos",
        "Batch API disponible"
    ]
}
```

### 3. **Balance Costo-Calidad**
```python
{
    "modelo_primario": "gemini-2.5-flash",
    "razonamiento": "3x más barato que GPT-4o-mini en salida",
    "casos_uso": [
        "Facturas comerciales estándar",
        "Documentos con tablas",
        "Procesamiento multimodal"
    ]
}
```

## 💡 TIPS DE AHORRO

1. **Use Batch API de Gemini**: 50% descuento en todos los modelos
2. **Implemente Cache**: 
   - OpenAI: 50% descuento en entrada
   - Gemini: Hasta 90% descuento en entrada cacheada
3. **Escalonamiento Inteligente**:
   ```python
   if documento_simple:
       use("gemini-2.5-flash-lite")  # $0.0001/1K
   elif documento_medio:
       use("gpt-4o-mini")            # $0.00015/1K
   else:  # documento_complejo
       use("gemini-2.5-pro")         # $0.00125/1K
   ```

## 📊 RESUMEN EJECUTIVO

**🏆 Ganador por Categoría:**
- **Más Económico**: Gemini 2.5 Flash-Lite ($0.10/1M tokens)
- **Mejor Relación Precio/Calidad**: Gemini 2.5 Flash ($0.30/1M tokens)
- **Mayor Contexto**: Gemini 2.5 Pro (2M tokens)
- **Mejor para Código**: GPT-4o ($2.50/1M tokens)
- **Más Rápido y Barato**: Gemini 2.5 Flash-Lite

**💰 Potencial de Ahorro:**
- Cambiar de GPT-4o a Gemini 2.5 Flash-Lite: **96% de ahorro**
- Cambiar de GPT-4o-mini a Gemini 2.5 Flash-Lite: **33% de ahorro**
- Usar Batch API: **50% adicional de descuento**

---
*Nota: Precios actualizados a Octubre 2025. Los precios pueden variar según región y volumen.*



# Ejemplo: Tienda que procesa facturas
```bash
volumen_mensual = {
    "pequeño_negocio": {
        "facturas": 1000,
        "modelo": "Gemini 2.5 Flash-Lite",
        "costo": "$0.13 USD/mes"
    },
    "negocio_mediano": {
        "facturas": 10000,
        "modelo": "Gemini 2.5 Flash-Lite",
        "costo": "$1.30 USD/mes"
    },
    "empresa_grande": {
        "facturas": 100000,
        "modelo": "Gemini 2.5 Flash-Lite",
        "costo": "$13.00 USD/mes"
    }
}

# Si implementas Prompt Caching
volumen_con_cache = {
    "pequeño_negocio": {
        "facturas": 1000,
        "costo_sin_cache": "$0.13",
        "costo_con_cache": "$0.065 USD/mes"  # ← Aquí sí aplica el descuento
    },
    "negocio_mediano": {
        "facturas": 10000,
        "costo_sin_cache": "$1.30",
        "costo_con_cache": "$0.65 USD/mes"
    },
    "empresa_grande": {
        "facturas": 100000,
        "costo_sin_cache": "$13.00",
        "costo_con_cache": "$6.50 USD/mes"
    }
}
```

---

## 🎯 RESUMEN EJECUTIVO

**Para tu caso (tiempo real, sin batch):**

| Volumen | Gemini 2.5 Flash-Lite | Con Cache | GPT-4o-mini | GPT-4o |
|---------|----------------------|-----------|-------------|--------|
| **1K facturas** | $0.13 | $0.065 | $0.195 | $3.25 |
| **10K facturas** | $1.30 | $0.65 | $1.95 | $32.50 |
| **100K facturas** | $13.00 | $6.50 | $19.50 | $325.00 |

**Recomendación:**
```
✅ Usar: Gemini 2.5 Flash-Lite
💰 Costo inicial: $0.13 por 1,000 facturas
🚀 Optimizado con cache: $0.065 por 1,000 facturas
📊 Es 25x más barato que GPT-4o
⚡ Respuesta en 2-5 segundos