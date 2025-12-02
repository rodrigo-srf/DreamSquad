import os
import math
from dotenv import load_dotenv
from strands_agents import Agent, OllamaLLM, Tool
from pydantic import BaseModel, Field

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do LLM (Ollama)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
STRANDS_API_KEY = os.getenv("STRANDS_API_KEY") # Chave necessária para o SDK

# 2. Implementação da Tool de Cálculo Matemático (Requisito 3.2)
class MathToolInput(BaseModel):
    """Schema Pydantic para a entrada da Tool de Cálculo."""
    expression: str = Field(description="A expressão matemática a ser avaliada, por exemplo, '1234 * 5678' ou 'math.sqrt(144)'.")

@Tool(
    name="calculator",
    description="Útil para operações matemáticas como adição, subtração, multiplicação, divisão e raiz quadrada. Use sintaxe Python.",
    input_schema=MathToolInput
)
def calculator_tool(expression: str) -> str:
    """Executa uma expressão matemática simples de forma controlada."""
    try:
        # Permite apenas funções seguras e básicas do módulo math
        allowed_names = {
            'sqrt': math.sqrt, 'pow': math.pow, 'pi': math.pi, 'e': math.e,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan
        }
        
        # Avalia a expressão com escopo limitado
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return f"O resultado de {expression} é: {result}"
    except Exception as e:
        return f"Erro ao calcular a expressão. Certifique-se de que a sintaxe está correta: {e}"


# 3. Instanciação do LLM e do Agente (Requisito 3.1)
llm = OllamaLLM(
    api_base=f"{OLLAMA_HOST}/api",
    model=OLLAMA_MODEL,
    # A API Key pode ser necessária, mesmo com Ollama local, dependendo da configuração do Strands
    api_key=STRANDS_API_KEY
)

# Cria o Agente com o LLM e a Tool
chat_agent = Agent(
    llm=llm,
    tools=[calculator_tool], # Associa a Tool
    name="MathSolverAgent",
    description="Um agente que pode responder a perguntas gerais e usar uma ferramenta de cálculo (calculator) para resolver problemas matemáticos."
)

# 4. Função principal de atendimento
async def ask_agent(prompt: str) -> str:
    """Invoca o Strands Agent com o prompt do usuário."""
    # Usa o método assíncrono 'run' do Strands Agent
    try:
        response = await chat_agent.run(prompt=prompt)
        # O agente decide se usa a Tool ou responde diretamente
        return response.content
    except Exception as e:
        return f"Erro na execução do Agente (Verifique se o Ollama está rodando e o modelo baixado): {e}"