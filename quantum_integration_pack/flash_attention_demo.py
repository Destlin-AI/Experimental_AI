
from flash_attn import flash_attention
import torch

q = torch.rand(1, 64, 64)
k = torch.rand(1, 64, 64)
v = torch.rand(1, 64, 64)

attn = flash_attention(q, k, v)
print("⚡ Flash Attention Output:", attn)
