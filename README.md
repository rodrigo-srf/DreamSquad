🧠 API de Chat com Agente de IA (FastAPI + Ollama)

Este projeto implementa uma API web usando FastAPI integrada a um agente de IA local rodando no Ollama.
O objetivo é permitir que consultas feitas à API sejam respondidas por um modelo de linguagem instalado localmente.

---

🚀 Tecnologias usadas

 Python 3.10+
 FastAPI
 Uvicorn
 Ollama (modelo local)
 Requests / httpx

---

📦 Instalação

1. Instale dependências

```bash
pip install fastapi uvicorn httpx python-dotenv
```

2. Instale e rode o Ollama

Baixe e instale o Ollama pela página oficial:

👉 [https://ollama.com/download](https://ollama.com/download)

Verifique se está funcionando:

```bash
ollama --version
```

Liste os modelos:

```bash
ollama list
```

Baixe um modelo (exemplo):

```bash
ollama pull qwen2.5:1.5b
```

Teste:

```bash
ollama run qwen2.5:1.5b
```

Se aparecer o prompt `>>>`, está OK.

---

🔌 Configuração do ambiente

Crie um arquivo `.env` na raiz do projeto:

```
OLLAMA_MODEL=qwen2.5:1.5b
OLLAMA_HOST=http://localhost:11434
```

---

🧩 Código da API (main.py)

Crie o arquivo `main.py` com este conteúdo:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

app = FastAPI(title="Chat API + Agente IA")

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(payload: ChatMessage):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": payload.message}
        )

        data = response.json()
        return {"response": data.get("response", "Erro ao gerar resposta")}
```

---

▶️ Executar a API

Agora rode:

```bash
uvicorn main:app --reload
```

A API estará disponível em:

👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Documentação automática:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

🧪 Teste da API (Exemplo)

POST → `/chat`

Body JSON:

```json
{
  "message": "Explique a teoria da relatividade em 1 frase"
}
```

Resposta:

```json
{
  "response": "A relatividade descreve como tempo e espaço mudam conforme a velocidade e a gravidade."
}
```

---

🔍 Como funciona tecnicamente?

1. O **Ollama** roda localmente ouvindo na porta **11434**.
2. A **FastAPI** recebe mensagens via `/chat`.
3. A API chama o endpoint:

   ```
   POST http://localhost:11434/api/generate
   ```
4. O modelo responde e a API retorna a resposta ao cliente.
5. Não é necessário expor IP — o Ollama é local e a API fala com ele via HTTP interno.

---

📁 Estrutura final do projeto

```
CHAT-AGENT-CASE/
 ├── __pycache__/
 ├── venv/
 ├── .env
 ├── .env.example
 ├── .gitignore
 ├── agent.py
 ├── LICENSE
 ├── main.py
 ├── README.md
 ├── requirements.txt
 └── run_demo.sh

```
