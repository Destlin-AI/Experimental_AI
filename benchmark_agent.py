
import time
import random
import psutil
import threading

results = {}

def simulate_fragment_walks(num_fragments, walk_speed_per_sec):
    walks_done = 0
    start_time = time.time()
    end_time = start_time + 10
    while time.time() < end_time:
        walks_done += walk_speed_per_sec
        time.sleep(1)
    results['walks'] = walks_done

def simulate_mutation_ops(rate_per_sec):
    mutations_done = 0
    start_time = time.time()
    end_time = start_time + 10
    while time.time() < end_time:
        mutations_done += rate_per_sec
        time.sleep(1)
    results['mutations'] = mutations_done

def simulate_emotion_decay_ops(fragments_count, decay_passes_per_sec):
    decay_ops_done = 0
    start_time = time.time()
    end_time = start_time + 10
    while time.time() < end_time:
        decay_ops_done += decay_passes_per_sec
        time.sleep(1)
    results['decay'] = decay_ops_done

def run():
    walk_thread = threading.Thread(target=simulate_fragment_walks, args=(10000, random.randint(200, 350)))
    mutate_thread = threading.Thread(target=simulate_mutation_ops, args=(random.randint(30, 60),))
    decay_thread = threading.Thread(target=simulate_emotion_decay_ops, args=(10000, random.randint(50, 100)))

    walk_thread.start()
    mutate_thread.start()
    decay_thread.start()

    walk_thread.join()
    mutate_thread.join()
    decay_thread.join()

    results['cpu_usage_percent'] = psutil.cpu_percent(interval=1)
    results['ram_usage_percent'] = psutil.virtual_memory().percent

    print("===== Symbolic TPS Benchmark =====")
    print(f"Fragment Walks     : {results['walks'] // 10} per second")
    print(f"Mutations          : {results['mutations'] // 10} per second")
    print(f"Emotion Decay Ops  : {results['decay'] // 10} per second")
    print()
    print(f"CPU Usage          : {results['cpu_usage_percent']}%")
    print(f"RAM Usage          : {results['ram_usage_percent']}%")
    print("==================================")

if __name__ == "__main__":
    run()
