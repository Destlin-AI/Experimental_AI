import psutil
import platform
import shutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = shutil.disk_usage("C:\")

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        gpu_info = [{"name": gpu.name, "load": gpu.load * 100, "mem_used": gpu.memoryUsed, "mem_total": gpu.memoryTotal} for gpu in gpus]
    except:
        gpu_info = [{"error": "GPUtil not available or no GPU found."}]

    return {
        "cpu_percent": cpu_usage,
        "ram_total": ram.total // (1024 ** 2),
        "ram_used": ram.used // (1024 ** 2),
        "disk_total": disk.total // (1024 ** 3),
        "disk_used": disk.used // (1024 ** 3),
        "platform": platform.system(),
        "gpu": gpu_info
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_info(), indent=2))
