import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def ask_model(prompt: str, model="qwen2.5:1.5b"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()
    return data.get("response", "(sem resposta)")
