from json import loads
import src.config as config
import src.constants as constants
from kafka import KafkaConsumer
from src.producer import Producer

non_articles_producer = Producer('non-articles-input')
plain_text_producer = Producer('plain-text-articles-input')

consumer = KafkaConsumer(
    'plaintext-input',
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='plain_text_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))


def main():
    print('started consumer')

    for message in consumer:
        message = message.value
        print(message)
        # TODO: use machine learing to check if it's an article and publish it to the right topic


if __name__ == "__main__":
        main()
