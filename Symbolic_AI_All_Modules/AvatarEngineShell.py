# === MODULE: AvatarEngineShell ===

class AvatarEngineShell:
    def __init__(self):
        self.expressions = {}
        self.context_state = {}

    def inject_expression(self, label, script):
        self.expressions[label] = script
        print(f"[🎭] Expression loaded: {label}")

    def execute(self, label, data):
        expr = self.expressions.get(label)
        if not expr:
            return f"[❌] No expression for: {label}"
        print(f"[🗣️] Running avatar expression: {label}")
        return expr(data)
