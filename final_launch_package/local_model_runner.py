from llama_cpp import Llama

# Adjust path if your model is not in the current directory
MODEL_PATH = "Llama-3-8B-Instruct-Gradient-1048k-Q3_K_S.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    use_mlock=True,
)

def run_local_llm(prompt: str, max_tokens: int = 256) -> str:
    result = llm(prompt, max_tokens=max_tokens)
    return result["choices"][0]["text"].strip()

# Test call (you can remove this block in production)
if __name__ == "__main__":
    response = run_local_llm("What is synthetic memory?")
    print("LLM Response:", response)