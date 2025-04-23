from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from ollama_client import run_ollama

app = FastAPI()

# Allow frontend (Electron or local web) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "🟢 Backend running", "path": os.getcwd()}

@app.post("/query")
async def query_llm(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    model = data.get("model", "llama3")
    response = run_ollama(prompt, model)
    return {"response": response or "[❌] Failed to get response"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
