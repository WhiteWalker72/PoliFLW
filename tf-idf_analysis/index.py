import src.persistence.article_service as articles_service
from kafka import KafkaConsumer
import src.config as config
import src.constants as constants
from json import loads
from src.producer import Producer
import src.api.service as api
from threading import Thread
from src.analysis import Analysis

TFIDF_TOPIC = 'tfidf-input'
UNIQUE_TOPIC = 'unique-articles-input'
analysis = Analysis()

unique_consumer = KafkaConsumer(
    UNIQUE_TOPIC,
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='articles_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))

tfidf_producer = Producer(TFIDF_TOPIC)


def format_message(message):
    message['title'] = ' '.join(message['title'])
    message['text'] = ' '.join(message['text'])
    return message


def publish_message(message):
    message.pop('_id', None)
    tfidf_producer.send_message(message)


def start_consumer():
    print('Started ' + UNIQUE_TOPIC + ' consumer')

    for message in unique_consumer:
        message = format_message(dict(message.value))
        url = message['url']
        text = message['text']

        dataframe = analysis.get_dataframe_from_json(text)

        tfidf_dateframe = analysis.get_tfidf_from_dataframe(dataframe)
        tfidf_json = tfidf_dateframe.to_json(orient='records')

        # TODO: Store this JSON


def main():
    api_thread = Thread(target=api.start_api)
    api_thread.start()
    consumer_thread = Thread(target=start_consumer)
    consumer_thread.start()


if __name__ == "__main__":
    main()
