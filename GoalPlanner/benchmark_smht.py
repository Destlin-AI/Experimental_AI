import time
from smht_core import SMHTCore

def benchmark(model, tokens, iterations=100):
    total_time = 0
    for _ in range(iterations):
        start = time.perf_counter()
        model.run_inference(tokens)
        total_time += time.perf_counter() - start
    avg_time = total_time / iterations
    print(f"Tokens: {tokens} | Iterations: {iterations}")
    print(f"Avg inference time: {avg_time:.6f} sec")

if __name__ == "__main__":
    engine = SMHTCore()
    benchmark(engine, ["hello", "world", "goodbye"], 100)