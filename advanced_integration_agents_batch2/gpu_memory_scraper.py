
import pynvml
pynvml.nvmlInit()

def get_gpu_memory():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    print(f"🎮 GPU Mem Used: {info.used / 1024**2:.2f} MB")

if __name__ == "__main__":
    get_gpu_memory()
