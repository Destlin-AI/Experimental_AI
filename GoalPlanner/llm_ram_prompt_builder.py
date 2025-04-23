# === BATCH 7: llm_ram_prompt_builder.py ===

import os
from pathlib import Path

RAM_CACHE = Path("D:/Project_AI/meta/hotcache")

def assemble_context(query_topic: str, top_k=10):
    gathered = []
    for cache_file in RAM_CACHE.glob("*_cache.txt"):
        with open(cache_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if query_topic.lower() in line.lower():
                    gathered.append(line.strip())
                    if len(gathered) >= top_k:
                        break
    prompt = f"""
You are a symbolic AI with high-recall lateral memory. Context below:

{chr(10).join(gathered)}

Respond precisely and only from the above context.
"""
    return prompt

if __name__ == "__main__":
    print(assemble_context("memory inference"))
