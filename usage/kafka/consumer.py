import json
from kafka import KafkaConsumer


def decode(v):
    if not isinstance(v, (str, bytes, bytearray)):
        return
    try:
        data = json.loads(v)
    except ValueError:
        return
    return data


class Consumer:

    def __init__(self, brokers, group_id):
        self.client: KafkaConsumer = KafkaConsumer(
            bootstrap_servers=brokers,
            value_deserializer=decode,
            group_id=group_id,
            api_version=(2, 5),
        )

    def subscribe(self, topics):
        self.client.subscribe(topics)

    def is_connected(self):
        return self.client.bootstrap_connected()

    def close(self):
        if self.is_connected():
            return self.client.close()

    def __iter__(self):
        return iter(self.client)
