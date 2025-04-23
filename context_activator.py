import yaml
from pathlib import Path

FRAGMENTS_DIR = Path("fragments/core")
ACTIVATION_LOG = Path("logs/context_activation.log")
ACTIVATION_LOG.parent.mkdir(parents=True, exist_ok=True)

class ContextActivator:
    def __init__(self, activation_threshold=0.75):
        self.threshold = activation_threshold

    def scan_fragments(self):
        activated = []
        for frag_file in FRAGMENTS_DIR.glob("*.yaml"):
            try:
                with open(frag_file, 'r') as f:
                    frag = yaml.safe_load(f)
                if frag.get("confidence", 0.5) >= self.threshold:
                    activated.append(frag)
            except Exception as e:
                print(f"Error reading {frag_file.name}: {e}")
        return activated

    def log_activations(self, activations):
        with open(ACTIVATION_LOG, 'a') as log:
            for frag in activations:
                log.write(f"[ACTIVATED] {frag['id']} :: {frag.get('claim', '???')}\n")
        print(f"[ContextActivator] {len(activations)} fragment(s) activated.")

    def run(self):
        active = self.scan_fragments()
        self.log_activations(active)

if __name__ == "__main__":
    ctx = ContextActivator()
    ctx.run()
