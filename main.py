from fastapi import FastAPI
from agent import ask_model

app = FastAPI()

@app.post("/chat")
def chat(message: str):
    response = ask_model(message)
    return {"response": response}
