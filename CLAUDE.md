# CLAUDE.md — Plataforma Multi-Agente B2B para Soporte Operativo (TFM)

> Documento de contexto para Claude Code y para el proyecto de Claude.ai.
> Mantener actualizado conforme avanza el desarrollo (ver sección "Mantenimiento de este documento").

## 1. Identidad del proyecto

- **Nombre:** Plataforma Multi-Agente B2B para Soporte Operativo
- **Tipo:** Trabajo Fin de Máster (TFM) — Máster en IA Generativa Avanzada
- **Alumno:** Juan Archidona Ahijado
- **Repositorio GitHub:** https://github.com/JuanArchidona/multi-agent-support-platform (rama `master`)
- **Estado actual:** Fase de arranque / *scaffolding*. Entorno montado y conexiones a proveedores de IA validadas. La lógica de negocio (agentes, RAG, orquestación) **aún NO está implementada**.

## 1.1 Fase académica y temporal (actualizado: 14 jun 2026)

- **Hoy:** 14 de junio de 2026. Cursando **Módulo 2** del máster (Arquitecturas y Orquestación: RAG avanzado, BD vectoriales, multi-agente con LangGraph, MCP).
- **Por delante:** Módulo 3 (LLMOps: observabilidad, evaluación) y Módulo 4 (Gobernanza/Seguridad: EU AI Act, guardrails, PII). Estos módulos cubren justo las piezas hoy abiertas del proyecto.
- **TFM (Módulo 5):** se desarrolla en **septiembre 2026** y se defiende en **octubre 2026**.
- **Implicación de trabajo:** ahora mismo es fase de **aprendizaje (Módulo 2) y scaffolding conceptual**, no de productivización. Lo accionable hoy es el **núcleo de orquestación y RAG** (grafo, BD vectoriales, chunking/ranking, LangGraph). Las decisiones de productivización (checkpointer, multi-tenant, guardrails, PII, observabilidad) se cierran **cuando llegue su módulo o la fase del TFM**, no antes. No introducir deuda conceptual de módulos futuros.

## 2. Concepto del producto

Sistema **SaaS transversal y agnóstico de sector** que permite a cualquier **PYME** conectar:
- Su **base documental** (PDFs, manuales, contratos, políticas) → datos **no estructurados** (RAG).
- Su **base de datos de negocio** (CRM/ERP/ticketing) → datos **estructurados** (API REST).

Un **escuadrón de agentes de IA** resuelve consultas complejas y automatiza tareas repetitivas para empleados internos o clientes finales de la PYME. El sistema es **omnicanal**: entrada/salida vía **Slack, Email o tickets (Zendesk)**.

## 3. Arquitectura funcional objetivo (flujo multi-agente)

```
Trigger → Clasificador → Recuperación → Generación → Guardrails → Output
```

1. **Trigger:** mensaje del usuario vía Slack, Webhook o Email.
2. **Clasificador (enrutamiento):** modelo ligero que detecta la intención.
3. **Recuperación (bifurcación según intención):**
   - Duda **documental** → base de datos **vectorial (RAG)**.
   - Duda **operativa/estado** → **API del CRM/ERP vía Function Calling**.
4. **Generación:** LLM principal redacta usando el contexto recuperado.
5. **Guardrails:** validación contra alucinaciones y exposición de info indebida.
6. **Output:** envío de la respuesta al canal de origen.

### Fuentes de datos asumidas
- **RAG / no estructurado:** PDFs/Word en cloud (AWS S3 o Google Drive).
- **Estructurado:** API REST a CRM (HubSpot/Salesforce) o ticketing (Zendesk).

### Componentes externos previstos
- **BD vectorial:** Pinecone o Chroma *(sin decidir)*.
- **Orquestador:** **LangGraph** (decisión tomada).
- **APIs de LLM:** Anthropic y Google.

## 4. Requisitos no funcionales y gobernanza

- **Latencia objetivo:** 3–8 s totales (sistema asíncrono/semi-síncrono). Cuello de botella = LLM de generación final.
- **Determinismo:** temperatura baja (0.1–0.2) en el System Prompt.
- **Estructura del prompt dinámico:** (1) rol del agente, (2) contexto inyectado (RAG o CRM), (3) consulta original, (4) restricciones estrictas ("no inventes información fuera del contexto").
- **Coste:** objetivo de céntimos por petición. **Prompt Caching de Anthropic** clave para abaratar documentos largos recurrentes.
- **Privacidad (PII):** filtro de anonimización previo (nombres, DNI, tarjetas) antes de enviar a LLMs de terceros. Sistema multi-cliente.
- **Human-in-the-loop:** ante alta sensibilidad o baja confianza, detener automatización y escalar a humano.

## 5. Decisión estratégica: código directo (no n8n)

Desarrollo directo en Python desde prototipo a producción. Motivos: control total de orquestación (LangGraph), acceso a SDK avanzado (Prompt Caching), selección de modelo por nodo, producción B2B desde el inicio y evitar deuda técnica de reescribir lógica.

## 6. Stack técnico

| Elemento | Decisión |
|---|---|
| IDE | Visual Studio Code |
| Lenguaje | Python 3.12 |
| Entorno/dependencias | **uv** (con `uv.lock`) |
| Orquestación prevista | LangGraph *(aún no instalado)* |
| Asistentes IA | Claude Code, GitHub Copilot |
| Control de versiones | Git + GitHub |

### Dependencias actuales (`pyproject.toml`)
- `anthropic>=0.104.1`
- `google-genai>=2.6.0`
- `python-dotenv>=1.2.2`

### Proveedores de IA validados
- **Google Gemini** (Google AI Studio) — `gemini-2.5-flash`. Uso: clasificación de intenciones, enrutamiento, tareas de propósito general (modelo ligero/barato).
- **Anthropic Claude** — `claude-haiku-4-5-20251001`. Uso: razonamiento complejo, lectura documental extensa (RAG), generación de código, con **Prompt Caching**.

> Estrategia por nodo: modelos ligeros (flash/haiku) en clasificación; modelos más capaces en generación final.

## 7. Estructura del repositorio

```
TFM/  (repo: multi-agent-support-platform)
├── main.py                  # Stub: imprime "Hello from tfm!"
├── src/
│   └── test_connection.py   # Valida conexión a Gemini y Anthropic desde .env
├── data/                    # Local (data/raw y data/processed ignorados en git)
├── notebooks/               # Vacío (exploración Jupyter)
├── docs/
│   └── generate_submission.py   # Genera PDF de entrega del máster (FPDF) — NO es producto
├── Documentación/           # PDFs de concepto/entorno (ignorado en git)
├── pyproject.toml
├── uv.lock
├── .env / .env.example      # GEMINI_API_KEY, ANTHROPIC_API_KEY
├── .python-version          # 3.12
├── .gitignore
└── CLAUDE.md                # Este documento
```

### Variables de entorno (`.env`, ignorado en git)
```
GEMINI_API_KEY=
ANTHROPIC_API_KEY=
```

## 8. Comandos útiles

```bash
uv sync                          # Instalar/actualizar dependencias del lock
uv run src/test_connection.py    # Validar conexión a Gemini y Anthropic
uv add <paquete>                 # Añadir dependencia
```

## 9. Roadmap inmediato (próximos pasos)

1. **Prompts iniciales:** System Prompt del clasificador y de los nodos especializados (RAG y CRM).
2. **Selección de modelos por nodo** para cumplir 3–8 s.
3. **Pipeline RAG:** ingesta y búsqueda vectorial sobre PDFs con Prompt Caching.
4. **Orquestación LangGraph:** grafo `trigger → clasificador → recuperación → generación → guardrails → output`.

## 10. Decisiones deliberadamente diferidas (no son olvidos)

Estas decisiones se cierran cuando lleguen al módulo correspondiente o a la fase del TFM. Listadas con el momento previsto:

| Decisión abierta | Se cierra en |
|---|---|
| BD vectorial: Pinecone vs Chroma | Módulo 2 / inicio TFM |
| Modelo de embeddings (OpenAI / Google / Voyage / self-hosted) | Módulo 2 / inicio TFM |
| Estrategia de chunking y re-ranking | Módulo 2 |
| Estrategia de Prompt Caching (system prompt vs contexto recuperado) | Módulo 2 |
| Estado/memoria del grafo: stateless vs checkpointer (Memory/Postgres/Redis) | Módulo 2–3 |
| Multi-tenancy: namespace vs índice vs metadata-filtering; `tenant_id` en el estado | Inicio TFM (sept 2026) |
| Backend/API del SaaS (FastAPI u otro) | Inicio TFM |
| Observabilidad / evaluación (LLMOps) | Módulo 3 |
| Guardrails, anonimización PII (regex/Presidio vs NER, reversibilidad), EU AI Act | Módulo 4 |
| Human-in-the-loop: `interrupt()` real vs bifurcación a cola humana | Módulo 4 / TFM |
| Integraciones de canal (Slack/Email/Zendesk) y conectores CRM | Fase TFM, según alcance del MVP |
| Modelo del nodo de generación (Haiku por coste vs Sonnet/Opus por capacidad) | Al construir el nodo de generación |
| LangGraph como dependencia | Al montar el primer grafo (Módulo 2) |

## 11. Mantenimiento de este documento

Mantener este `CLAUDE.md` como **fuente única de verdad** del contexto del proyecto:
- Al cerrar un avance relevante (nueva dependencia, decisión de arquitectura, nodo implementado), actualizar la sección correspondiente y la 9/10.
- Hacer commit del cambio junto al código (`git add CLAUDE.md && git commit`).
- `git push` para que el proyecto de Claude.ai (conectado al mismo repo de GitHub) lo recoja.
