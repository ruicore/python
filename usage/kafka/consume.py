
KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC = 'thing-data'
KAFKA_GROUP = 'thing-cockpit'

from consumer import Consumer


def consume_data(topic, borker, group_id):
    consumer = Consumer(brokers=[borker], group_id=group_id)

    consumer.subscribe([topic, "thing-event"])

    for msg in consumer:
        try:
            value = msg.value
            print(value)
        except Exception as err:
            print(err)
            continue


if __name__ == "__main__":
    consume_data(KAFKA_TOPIC, KAFKA_BROKER, KAFKA_GROUP)
