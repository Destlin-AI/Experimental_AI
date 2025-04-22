
import multiprocessing
import random
import time

def variant_logic(x):
    time.sleep(random.uniform(0.1, 0.5))
    return x**2 + random.randint(-3, 3)

if __name__ == "__main__":
    pool = multiprocessing.Pool(4)
    results = pool.map(variant_logic, range(10))
    best = max(results)
    print("🔥 Best Result:", best)
