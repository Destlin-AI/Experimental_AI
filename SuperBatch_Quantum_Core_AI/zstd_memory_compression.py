
import zstandard as zstd

cctx = zstd.ZstdCompressor(level=22)
with open("memory_block.bin", "rb") as f:
    memory = f.read()

compressed = cctx.compress(memory)
print(f"🗜️ Compressed size: {len(compressed)} bytes")
