
import pynvml
import hashlib
import time

pynvml.nvmlInit()

def hash_entropy_from_gpu():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    mem = pynvml.nvmlDeviceGetMemoryInfo(handle).used
    clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
    entropy_seed = f"{mem}_{clock}_{time.time()}".encode()
    entropy_hash = hashlib.sha512(entropy_seed).hexdigest()
    return entropy_hash

if __name__ == "__main__":
    while True:
        print("🔐 GPU Entropy:", hash_entropy_from_gpu())
        time.sleep(5)
