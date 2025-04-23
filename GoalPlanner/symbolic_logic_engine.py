class LogicTree:
    def __init__(self):
        self.rules = {"hello": "👋", "world": "🌍", "goodbye": "👋❌"}

    def resolve(self, token):
        return self.rules.get(token.lower(), f"[unknown:{token}]")