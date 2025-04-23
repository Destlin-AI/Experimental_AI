import subprocess
import json

def run_ollama(prompt: str, model: str = "llama3"):
    print(f"[🧠] Sending prompt to Ollama ({model})...")

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        if result.returncode != 0:
            print("[❌] Ollama error:", result.stderr.decode("utf-8"))
            return None

        output = result.stdout.decode("utf-8")
        print("[✅] LLM response received.")
        return output.strip()

    except subprocess.TimeoutExpired:
        print("[⚠️] Ollama call timed out.")
        return None
    except Exception as e:
        print(f"[💥] Unexpected error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    response = run_ollama("What is symbolic memory?")
    print(response or "[⚠️] No response.")
