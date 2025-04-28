from fastapi import FastAPI
from pydantic import BaseModel
import torch
import multiprocessing as mp

app = FastAPI()

# Shared task/result queues
task_queue = None
result_queue = None

class InferenceRequest(BaseModel):
    tensor_data: list
    tensor_shape: list

class InferenceResponse(BaseModel):
    output_data: list
    output_shape: list

@app.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    input_tensor = torch.tensor(request.tensor_data).reshape(request.tensor_shape).float()

    idx = id(input_tensor) % (2**31 - 1)  # Some pseudo-unique ID
    task_queue.put((idx, input_tensor.detach()))

    received_idx, output_tensor = result_queue.get()
    assert received_idx == idx, "Mismatch!"

    output_data = output_tensor.flatten().tolist()
    output_shape = list(output_tensor.shape)

    return InferenceResponse(output_data=output_data, output_shape=output_shape)

def init_bridge(tq, rq):
    global task_queue, result_queue
    task_queue = tq
    result_queue = rq

# For command line running:
if __name__ == "__main__":
    manager = mp.Manager()
    task_queue = manager.Queue()
    result_queue = manager.Queue()

    init_bridge(task_queue, result_queue)

    import uvicorn
    uvicorn.run("TensorDaemonBridge:app", host="127.0.0.1", port=5000, reload=True)
