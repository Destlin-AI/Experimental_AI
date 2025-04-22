
import hashlib
import random
import time

def entropy_loop():
    seed = str(time.time() * random.random()).encode()
    hashval = hashlib.sha512(seed).hexdigest()
    print("Entropy pulse:", hashval[:64])

if __name__ == "__main__":
    while True:
        entropy_loop()
        time.sleep(1)
