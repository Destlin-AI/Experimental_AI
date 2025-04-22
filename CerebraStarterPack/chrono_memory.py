import os, mmap, numpy as np
from multiprocessing import Pool, RawArray
from numba import njit, prange

NVME_PATH = '/mnt/nvme/ceres.dat'
MEMORY_SIZE = 1_000_000_000

quantum_state = RawArray('Q', 256)

@njit(parallel=True, fastmath=True)
def quantum_hash(data):
    def recurse(d, depth):
        if depth == 0:
            return np.sum(d) % 2**64
        chunks = np.array_split(d, 4)
        r = np.empty(4, dtype=np.uint64)
        for i in prange(4): r[i] = recurse(chunks[i], depth-1)
        return (r[0]^r[1])+(r[2]|r[3])
    return recurse(data, 7)

class ChronoMemory:
    def __init__(self):
        self.fd = os.open(NVME_PATH, os.O_RDWR | os.O_CREAT)
        self.mem = mmap.mmap(self.fd, MEMORY_SIZE, access=mmap.ACCESS_WRITE)
        self.lock = np.zeros(1, dtype=np.int32)

    def _atomic_write(self, ptr, data):
        while np.compare_and_swap(self.lock, 0, 1): pass
        self.mem[ptr:ptr+len(data)] = data
        self.lock[0] = 0

    def store(self, key, value):
        qh = quantum_hash(np.frombuffer(key.encode(), dtype=np.uint8))
        self._atomic_write(qh % MEMORY_SIZE, value.encode())

    def retrieve(self, key):
        qh = quantum_hash(np.frombuffer(key.encode(), dtype=np.uint8))
        return self.mem[qh % MEMORY_SIZE:qh % MEMORY_SIZE + 256].tobytes().decode(errors='ignore')
