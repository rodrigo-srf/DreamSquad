from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask_agent # Importa a nova função assíncrona e corrigida

# Define o modelo de dados para o payload de entrada (Requisito 2.1)
class ChatMessage(BaseModel):
    message: str

app = FastAPI(title="Chat API + Agente IA com Strands Agents")

# Atualiza o endpoint para ser assíncrono e receber o payload JSON
@app.post("/chat")
async def chat(payload: ChatMessage):
    # Chama a função assíncrona do agente com a mensagem do payload
    # O payload.message garante que a mensagem venha do corpo JSON
    response = await ask_agent(payload.message)
    return {"response": response}