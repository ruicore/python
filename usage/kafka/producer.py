import json

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError


class Producer:
    def __init__(self, broker):
        self.client = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(1, 0),
            retries=3
        )

    def publish(self, topic, msg):
        try:
            future = self.client.send(topic, msg)
            future.add_callback(self.on_sucess)
            future.add_errback(self.on_send_error)
        except KafkaTimeoutError as err:
            print(err)

    @staticmethod
    def on_sucess(record_metadata):
        print(record_metadata.topic, record_metadata.offset)

    @staticmethod
    def on_send_error(exc):
        print(exc)
