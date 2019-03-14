import src.persistence.articles_service as articles_service
from kafka import KafkaConsumer
import src.config as config
import src.constants as constants
from json import loads
from src.producer import Producer
from src.similarity import is_similar

ARTICLES_TOPIC = 'articles-input'
UNIQUE_TOPIC = 'unique-articles-input'
MONGO_MIN_SIMILARITY_SCORE = 10
MIN_SIMILARITY_SCORE = 0.9
SIMILAR_ARTICLES_LIMIT = 5

unfiltered_consumer = KafkaConsumer(
    ARTICLES_TOPIC,
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='articles_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))

unique_producer = Producer(UNIQUE_TOPIC)


def format_message(message):
    message['title'] = ' '.join(message['title'])
    message['text'] = ' '.join(message['text'])
    return message


def publish_message(message):
    message.pop('_id', None)
    unique_producer.send_message(message)


def main():
    print('Started ' + ARTICLES_TOPIC + ' consumer')

    for message in unfiltered_consumer:
        message = format_message(dict(message.value))
        url = message['url']
        text = message['text']

        existing_article = articles_service.find_article(url)
        if existing_article is None:
            similar_articles = articles_service.find_similar_articles(
                text, 10, MONGO_MIN_SIMILARITY_SCORE
            )
            has_similar_article = False
            for article in similar_articles:
                if is_similar(article['text'], text, MIN_SIMILARITY_SCORE):
                    has_similar_article = True
                    break

            # article does not have any similar articles so insert it as a new article
            if not has_similar_article:
                articles_service.insert_article(message)
                publish_message(message)

        # replace the old article
        else:
            if existing_article['text'] != text:
                articles_service.delete_article(url)
                articles_service.insert_article(message)
                publish_message(message)


if __name__ == "__main__":
    main()
