# redis_subscriber.py
import redis

CHANNEL = "symbolic_channel"
client = redis.Redis(host='127.0.0.1', port=6379)
pubsub = client.pubsub()
pubsub.subscribe(CHANNEL)

print(f"🧏‍♂️ Listening on channel: {CHANNEL}")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"[SUB] {message['data'].decode('utf-8')}")
