# swarm_router.py — dispatch prompt to tiny LLMs + Queen via subprocess/threads

import subprocess
import threading
from flask import request

def call_ollama(model: str, prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

def route_prompt(prompt: str) -> str:
    # Placeholder for future swarm logic with parallel threads / toolcalls
    # Here: final call to Queen model
    return call_ollama("llama3", prompt)

def register_routes(app):
    @app.route("/api/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        prompt = data.get("prompt", "")
        response = route_prompt(prompt)
        return {"response": response}