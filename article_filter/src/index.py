from kafka import KafkaConsumer
import src.config as config
import src.constants as constants
from src.producer import Producer
from json import loads
from difflib import SequenceMatcher

ARTICLES_TOPIC = 'articles_input'
UNIQUE_TOPIC = 'unique-articles-input'
SIMILAR_RATIO = 0.8

unfiltered_consumer = KafkaConsumer(
    ARTICLES_TOPIC,
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='articles_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))

unique_producer = Producer(UNIQUE_TOPIC)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def similar_message_exists(new_message, ratio):
    return True
    # consumer = KafkaConsumer(
    #     UNIQUE_TOPIC,
    #     bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    #     auto_offset_reset='earliest',
    #     enable_auto_commit=False,
    #     group_id='unique_consumer',
    #     consumer_timeout_ms=300,
    #     value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))
    #
    # message_text = ' '.join(new_message['text'])
    #
    # for message in consumer:
    #     message = ' '.join(dict(message.value)['text'])
    #     if message == message_text:
    #         return True
    #     if similar(message, message_text) >= ratio:
    #         return True


def main():
    print('Started ' + UNIQUE_TOPIC + ' consumer')
    for message in unfiltered_consumer:
        message = dict(message.value)
        if not similar_message_exists(message, SIMILAR_RATIO):
            unique_producer.send_message(message)
            print('New message')
            print(message)
        else:
            print('Message already exists')
            print(message)


if __name__ == "__main__":
    main()
