import time

from producer import Producer

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC = 'thing-data'
KAFKA_GROUP = 'thing-cockpit'


if __name__ == '__main__':
    producer = Producer(KAFKA_BROKER)
    while True:
        data = {
            'timestamp': 1593834720000,
            'thing_id': 1,
            'company_id': 2,
            'data': {
                'production': 100,
            },
        }
        producer.publish(KAFKA_TOPIC, data)
        time.sleep(1)
