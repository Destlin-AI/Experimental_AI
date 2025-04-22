
import hashlib

history = set()

def break_loops(text):
    sig = hashlib.md5(text.encode()).hexdigest()
    if sig in history:
        print("⛔ Loop detected!")
    else:
        history.add(sig)
        print("✅ Fresh logic:", text)

if __name__ == "__main__":
    while True:
        s = input("Prompt: ")
        break_loops(s)
