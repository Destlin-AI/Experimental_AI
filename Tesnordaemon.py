import torch
import multiprocessing as mp
import psutil
import time
import os

# === SAFE SUBMITTER ===
def safe_submit(task_queue, input_tensor, microbatch_size=32):
    """
    Safely detaches and splits tensor into microbatches and queues them for processing.
    """
    input_tensor = input_tensor.detach().cpu()

    batch_size = input_tensor.size(0)
    for start_idx in range(0, batch_size, microbatch_size):
        end_idx = min(start_idx + microbatch_size, batch_size)
        microbatch = input_tensor[start_idx:end_idx]
        task_queue.put((start_idx, microbatch))

# === SAFE RECEIVER ===
def safe_receive(result_queue, expected_batches):
    """
    Safely receives results from the daemon and reassembles in correct order.
    """
    results = {}
    for _ in range(expected_batches):
        idx, out = result_queue.get()
        results[idx] = out
    output_tensor = torch.cat([results[i] for i in sorted(results.keys())])
    return output_tensor

# === PERSISTENT WORKER ===
def persistent_worker(model_state_dict, task_queue, result_queue, cpu_limit=85, worker_id=None):
    model = torch.nn.Sequential(
        torch.nn.Linear(512, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 128)
    )
    model.load_state_dict(model_state_dict)
    model.eval()

    if worker_id is not None:
        safe_cores = list(range(0, int(mp.cpu_count() * 0.85)))
        if worker_id < len(safe_cores):
            p = psutil.Process(os.getpid())
            p.cpu_affinity([safe_cores[worker_id]])

    while True:
        while psutil.cpu_percent(interval=0.1) > cpu_limit:
            time.sleep(0.05)

        item = task_queue.get()
        if item is None:
            break
        idx, micro_input = item
        micro_input = micro_input.detach()
        with torch.no_grad():
            output = model(micro_input)
        result_queue.put((idx, output.cpu().detach()))

# === DAEMON STARTER ===
def start_tensor_daemon(model, cpu_usage_limit=85):
    ctx = mp.get_context('spawn')
    task_queue = ctx.Queue()
    result_queue = ctx.Queue()

    total_cpus = mp.cpu_count()
    worker_count = max(1, int(total_cpus * (cpu_usage_limit / 100.0)))
    print(f"[TensorDaemon] Spawning {worker_count} workers (<= {cpu_usage_limit}% CPU load target).")

    model_state = model.state_dict()
    workers = []

    for i in range(worker_count):
        p = ctx.Process(target=persistent_worker, args=(model_state, task_queue, result_queue, cpu_usage_limit, i))
        p.start()
        workers.append(p)

    return task_queue, result_queue, workers

# === DAEMON SHUTDOWN ===
def shutdown_tensor_daemon(task_queue, workers):
    for _ in workers:
        task_queue.put(None)
    for p in workers:
        p.join()
    print("[TensorDaemon] Shutdown complete.")

# === FULL SYSTEM TEST ===
if __name__ == "__main__":
    print("🔥 Booting TensorDaemon Supreme Engine 🔥")

    # Dummy model (replace with your own!)
    model = torch.nn.Sequential(
        torch.nn.Linear(512, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 128)
    )

    task_queue, result_queue, workers = start_tensor_daemon(model, cpu_usage_limit=85)

    print("✅ TensorDaemon active. Ready for fire and forget.")

    try:
        while True:
            print("\n[System] Waiting for tensor tasks... (CTRL+C to stop)")
            time.sleep(10)  # Simulate idle waiting

            input_tensor = torch.randn(2048, 512, requires_grad=False)

            safe_submit(task_queue, input_tensor, microbatch_size=64)
            expected_batches = (input_tensor.size(0) + 63) // 64
            output_tensor = safe_receive(result_queue, expected_batches)

            print(f"[System] Full output shape: {output_tensor.shape}")

    except KeyboardInterrupt:
        print("\n🔻 Shutdown signal received. Killing TensorDaemon...")
        shutdown_tensor_daemon(task_queue, workers)
