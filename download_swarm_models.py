import subprocess

MODELS = [
    "tinydolphin:latest",
    "tinyllama:1.1b-chat",
    "mistral:instruct",
    "phi:2",
    "zephyr:7b-beta",
    "gemma:2b",
    "codellama:7b-instruct",
    "deepseek-coder:6.7b-instruct"
]

def pull_model(name):
    print(f"📦 Pulling: {name}")
    try:
        subprocess.run(["ollama", "pull", name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to pull {name} → {e}")

def list_models():
    print("\n✅ Installed Ollama Models:\n")
    subprocess.run(["ollama", "list"])

if __name__ == "__main__":
    for model in MODELS:
        pull_model(model)
    list_models()
