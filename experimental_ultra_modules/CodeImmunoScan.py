
import ast
import os

def scan_file(path):
    try:
        with open(path, "r") as f:
            content = f.read()
        tree = ast.parse(content)
        print(f"✅ Clean AST in: {path}")
    except Exception as e:
        print(f"⚠️ Anomaly in: {path} -> {str(e)}")

def recursive_scan(directory):
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                scan_file(os.path.join(root, f))

if __name__ == "__main__":
    recursive_scan(".")
