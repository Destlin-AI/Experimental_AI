import asyncio
import time
from collections import deque

class ContextManager:
    def __init__(self, window_size=64):
        self.token_window = deque(maxlen=window_size)

    def update(self, token):
        self.token_window.append(token)

    def get_context(self):
        return list(self.token_window)

async def stream_tokens(tokens, ctx_mgr):
    for token in tokens:
        ctx_mgr.update(token)
        await asyncio.sleep(0.01)  # simulate processing delay
        print(f"[Context] {ctx_mgr.get_context()}")

if __name__ == "__main__":
    ctx = ContextManager()
    asyncio.run(stream_tokens(["one", "two", "three", "four", "five"], ctx))