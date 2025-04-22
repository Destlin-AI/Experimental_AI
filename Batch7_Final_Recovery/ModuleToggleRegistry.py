
class ModuleToggleRegistry:
    def __init__(self):
        self.toggles = {}

    def register(self, name, default=False):
        self.toggles[name] = default
        print(f"[🧩] Module '{name}' registered: {'ON' if default else 'OFF'}")

    def toggle(self, name, state=None):
        if name in self.toggles:
            self.toggles[name] = not self.toggles[name] if state is None else state
            print(f"[⚙️] Toggled '{name}' → {'ON' if self.toggles[name] else 'OFF'}")

    def is_active(self, name):
        return self.toggles.get(name, False)
