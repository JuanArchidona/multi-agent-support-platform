from fpdf import FPDF

LEFT = 20
RIGHT = 20
WIDTH = 210 - LEFT - RIGHT

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

def h1(pdf, text):
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(20, 80, 160)
    pdf.set_x(LEFT)
    pdf.cell(WIDTH, 8, text, new_x="LEFT", new_y="NEXT")
    pdf.set_draw_color(20, 80, 160)
    pdf.set_line_width(0.4)
    pdf.line(LEFT, pdf.get_y(), LEFT + WIDTH, pdf.get_y())
    pdf.ln(3)

def h2(pdf, text):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(LEFT)
    pdf.multi_cell(WIDTH, 6, text)
    pdf.ln(1)

def body(pdf, text):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.set_x(LEFT)
    pdf.multi_cell(WIDTH, 5.5, text)
    pdf.ln(1)

def bullet(pdf, text):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.set_x(LEFT + 4)
    pdf.multi_cell(WIDTH - 8, 5.5, f"- {text}")

def row(pdf, label, value, color=(50, 50, 50)):
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(50, 6, label)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*color)
    pdf.multi_cell(WIDTH - 50, 6, value)

def code(pdf, lines):
    pdf.set_fill_color(240, 242, 246)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(1)
    for line in lines:
        pdf.set_x(LEFT)
        pdf.cell(WIDTH, 5, line, fill=True, new_x="LEFT", new_y="NEXT")
    pdf.ln(2)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_margins(LEFT, 20, RIGHT)

# CABECERA
pdf.set_fill_color(20, 80, 160)
pdf.rect(0, 0, 210, 36, "F")
pdf.set_y(9)
pdf.set_font("Helvetica", "B", 17)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 9, "Modulo 1.5: Configuracion del Entorno de Trabajo", align="C", new_x="LEFT", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 7, "Consumo Programatico", align="C", new_x="LEFT", new_y="NEXT")
pdf.ln(16)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 5, "Master IA Generativa Avanzada  |  Abril 2026  |  Alumno: Juan Archidona", align="C", new_x="LEFT", new_y="NEXT")
pdf.cell(0, 5, "Proyecto TFM: Plataforma Multi-Agente B2B para Soporte Operativo", align="C", new_x="LEFT", new_y="NEXT")
pdf.ln(7)

# 0. ESTRATEGIA
h1(pdf, "Estrategia Elegida: Desarrollo Directo en Codigo")
body(pdf, "La estrategia adoptada es el desarrollo directo en Python, desde el primer prototipo hasta la version de produccion.")
body(pdf, "Aunque n8n es una herramienta valida para validacion visual de flujos, la eleccion de codigo directo responde a razones tecnicas concretas:")
pdf.ln(1)
bullet(pdf, "Control total sobre la orquestacion: LangGraph permite gestionar el estado del agente, ciclos de razonamiento y bifurcaciones del flujo con una precision que no es posible en herramientas no-code.")
bullet(pdf, "Funcionalidades avanzadas de los proveedores: El Prompt Caching de Anthropic, esencial para reducir costes en el procesamiento recurrente de documentos RAG, requiere implementacion directa via SDK.")
bullet(pdf, "Gestion de latencia por nodo: El objetivo de 3-8 segundos de respuesta total exige seleccionar modelos distintos en cada nodo, lo que demanda control programatico.")
bullet(pdf, "Produccion B2B desde el inicio: El versionado, testing y seguridad necesarios para un entorno B2B real se gestionan mejor desde el codigo.")
bullet(pdf, "Sin deuda tecnica: Construir primero en n8n y migrar despues implica desarrollar la logica dos veces.")

# 1. ENTORNO
h1(pdf, "1. Entorno de Desarrollo")
row(pdf, "IDE:", "Visual Studio Code")
row(pdf, "Lenguaje:", "Python 3.12")
row(pdf, "Gestor de entorno:", "uv (dependencias + entorno virtual)")
row(pdf, "Orquestacion prevista:", "LangGraph")
row(pdf, "Extensiones de IA:", "Claude Code, GitHub Copilot")

# 2. PROVEEDORES
h1(pdf, "2. Proveedores de IA y Credenciales")
h2(pdf, "Google Gemini (via Google AI Studio)")
row(pdf, "Uso previsto:", "Clasificacion de intenciones, enrutamiento y tareas de proposito general")
row(pdf, "Modelo validado:", "gemini-2.5-flash")
row(pdf, "Estado:", "API Key generada y conexion programatica validada [OK]", (0, 140, 70))
pdf.ln(2)
h2(pdf, "Anthropic Claude")
row(pdf, "Uso previsto:", "Razonamiento complejo, lectura documental extensa (RAG) y generacion de codigo.")
body(pdf, "    La funcionalidad de Prompt Caching sera clave para reducir costes al procesar manuales tecnicos largos de forma recurrente.")
row(pdf, "Modelo validado:", "claude-haiku-4-5-20251001")
row(pdf, "Estado:", "API Key integrada y conexion programatica validada [OK]", (0, 140, 70))

# 3. REPOSITORIO
h1(pdf, "3. Control de Versiones y Repositorio")
row(pdf, "Plataforma:", "GitHub")
row(pdf, "Repositorio:", "https://github.com/JuanArchidona/multi-agent-support-platform", (20, 80, 160))
row(pdf, "Estado:", "Inicializado y operativo [OK]", (0, 140, 70))
pdf.ln(2)
body(pdf, "Estructura de carpetas implementada:")
code(pdf, [
    "multi-agent-support-platform/",
    "  src/           # Codigo fuente",
    "  data/          # Datos locales (excluidos de git)",
    "  docs/          # Documentacion tecnica",
    "  notebooks/     # Jupyter notebooks de exploracion",
    "  .env.example   # Plantilla de variables de entorno",
    "  .gitignore     # API keys, .venv y datos excluidos",
    "  pyproject.toml # Dependencias del proyecto",
    "  uv.lock        # Versiones exactas (reproducibilidad)",
])

# 4. VALIDACION
h1(pdf, "4. Validacion de Conexiones Programaticas")
body(pdf, "Script src/test_connection.py - valida la conexion a ambos proveedores cargando las credenciales desde .env:")
code(pdf, [
    "import os",
    "from dotenv import load_dotenv",
    "from google import genai",
    "import anthropic",
    "",
    "load_dotenv()",
    "",
    "def test_gemini():",
    "    os.environ.pop('GOOGLE_API_KEY', None)",
    "    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])",
    "    response = client.models.generate_content(",
    "        model='gemini-2.5-flash',",
    "        contents='Devuelve solo la palabra Gemini OK si me recibes.',",
    "    )",
    "    print(f'Gemini:    {response.text.strip()}')",
    "",
    "def test_anthropic():",
    "    client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])",
    "    response = client.messages.create(",
    "        model='claude-haiku-4-5-20251001',",
    "        max_tokens=16,",
    "        messages=[{'role': 'user', 'content': 'Devuelve solo la palabra Claude OK si me recibes.'}],",
    "    )",
    "    print(f'Anthropic: {response.content[0].text.strip()}')",
    "",
    "if __name__ == '__main__':",
    "    test_gemini()",
    "    test_anthropic()",
])
h2(pdf, "Comando de ejecucion:")
code(pdf, ["uv run src/test_connection.py"])
h2(pdf, "Resultado obtenido:")
code(pdf, ["Gemini:    Gemini OK", "Anthropic: Claude OK"])
body(pdf, "Ambos proveedores responden correctamente. El entorno esta completamente operativo para el consumo programatico.")

# 5. PROXIMOS PASOS
h1(pdf, "5. Proximos Pasos")
bullet(pdf, "Diseno de prompts iniciales - Definir el System Prompt del agente clasificador de intenciones y los prompts de los nodos especializados (RAG documental y consulta CRM).")
bullet(pdf, "Seleccion de modelos por nodo - Asignar modelos ligeros (flash/haiku) en clasificacion y enrutamiento, y modelos mas capaces en generacion final, para cumplir el objetivo de 3-8 segundos de latencia total.")
bullet(pdf, "Pipeline RAG - Implementar la ingesta y busqueda vectorial sobre documentos PDF con Prompt Caching habilitado.")
bullet(pdf, "Orquestacion con LangGraph - Implementar el flujo multi-agente: trigger -> clasificador -> recuperacion -> generacion -> guardrails -> output.")

output_path = r"C:\Users\Z00583TY\Desktop\Master\TFM\docs\entrega_modulo_1_5.pdf"
pdf.output(output_path)
print(f"PDF generado: {output_path}")