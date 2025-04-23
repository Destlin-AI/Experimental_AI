# redis_publisher.py
import redis
import time

CHANNEL = "symbolic_channel"
client = redis.Redis(host='127.0.0.1', port=6379)

def publish_loop():
    i = 0
    while True:
        message = f"🧠 Belief-{i} has entered the bus."
        client.publish(CHANNEL, message)
        print(f"[PUB] {message}")
        time.sleep(2)
        i += 1

if __name__ == "__main__":
    print(f"📡 Publishing on channel: {CHANNEL}")
    publish_loop()
