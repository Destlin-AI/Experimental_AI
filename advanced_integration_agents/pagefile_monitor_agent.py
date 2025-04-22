
import psutil

def monitor_pagefile():
    vm = psutil.virtual_memory()
    print(f"Pagefile used: {vm.total - vm.available} / {vm.total}")

if __name__ == "__main__":
    monitor_pagefile()
