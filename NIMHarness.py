# === MODULE: NIMHarness ===

class NIMHarness:
    def __init__(self):
        self.model_slots = {}

    def register_model(self, name, model):
        self.model_slots[name] = model
        print(f"[🧠] Registered model '{name}' into NIM Harness")

    def call(self, name, prompt):
        model = self.model_slots.get(name)
        if not model:
            return f"[❌] Model '{name}' not found."
        print(f"[🔁] Calling model '{name}' with prompt: {prompt[:40]}...")
        return model.generate(prompt) if hasattr(model, 'generate') else model(prompt)
