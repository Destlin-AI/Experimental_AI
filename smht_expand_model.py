import gzip
import os

def expand_model(output_path, scale_factor=10000):
    base = b"EXPANDED_MODEL_TOKEN"
    with gzip.open(output_path, "wb") as f:
        for _ in range(scale_factor):
            f.write(base)

if __name__ == "__main__":
    os.makedirs("models/unified", exist_ok=True)
    expand_model("models/unified/model.smhtz")
    print("Model expanded.")