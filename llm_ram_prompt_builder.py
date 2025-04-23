# llm_ram_prompt_builder.py
import json
from pathlib import Path

RAM_CACHE = Path("C:/real_memory_system/cache/ram_fragments.json")

def build_prompt_from_ram(task, token_limit=16000):
    with open(RAM_CACHE, "r", encoding="utf-8") as f:
        frags = json.load(f)

    output = []
    total_chars = 0
    for f in frags:
        chunk = f"# {f['timestamp']} [{', '.join(f['tags'])}] ({f['sub']})\n{f['claim']}\n{f['content']}\n"
        total_chars += len(chunk)
        if total_chars > token_limit * 4:
            break
        output.append(chunk)

    prompt = "\n\n".join(output)
    prompt += f"\n\n### TASK\n{task}"
    return prompt

if __name__ == "__main__":
    test = build_prompt_from_ram("Improve nested VM fault tolerance")
    print(test[:2000])
