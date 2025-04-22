import subprocess

def get_llm_status():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            timeout=10,
            text=True
        )
        if result.returncode != 0:
            return {"status": "offline", "error": result.stderr}
        return {"status": "online", "models": result.stdout}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    print(get_llm_status())
