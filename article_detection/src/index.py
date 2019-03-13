from json import loads
import src.config as config
import src.constants as constants
from kafka import KafkaConsumer
from src.producer import Producer
from src.detection import Detection

non_articles_producer = Producer('non-articles-input')
articles_producer = Producer('articles-input')

consumer = KafkaConsumer(
    'unfiltered-articles-input',
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='unfiltered_articles_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))


def main():
    detection = Detection()

    print(detection.is_political('De EASA'))
    print(detection.is_political('De VVD'))
    print('started consumer')

    for message in consumer:
        message = dict(message.value)
        if detection.is_political(message['text']):
            articles_producer.send_message(message)
        else:
            non_articles_producer.send_message(message)


if __name__ == "__main__":
        main()
