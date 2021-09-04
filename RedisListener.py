import redis
redis_url = 'redis://localhost:6379/0'
channel = 'logger'

class PubSubListener(object):
    def __init__(self):
        self.clients = []
        self.pubsub = redis.StrictRedis.from_url(redis_url, decode_responses=True).pubsub(ignore_subscribe_messages=False)
        self.pubsub.subscribe(**{channel: self.handler})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)

    def register(self, client):
        self.clients.append(client)

    def handler(self, message):
        _message = message['data']
        print(_message)
        if type(_message) != int:
            self.send(_message)

    def send(self, data):
        for client in self.clients:
            try:
                client.send(data)
            except Exception:
                self.clients.remove(client)