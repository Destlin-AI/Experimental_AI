# assemble_prompt.py — builds final string fed into LLM from memory fragments

def format_fragments(fragments: list[tuple]) -> str:
    prompt_block = []
    for frag in fragments:
        claim, content, tags = frag[1], frag[4], ", ".join(frag[3])
        prompt_block.append(f"Claim: {claim}\nTags: {tags}\n{content}\n---")
    return "\n".join(prompt_block)