import src.persistence.articles_service as articles_service
from kafka import KafkaConsumer
import src.config as config
import src.constants as constants
from json import loads

ARTICLES_TOPIC = 'articles-input'
MIN_SIMILARITY_SCORE = 10

unfiltered_consumer = KafkaConsumer(
    ARTICLES_TOPIC,
    bootstrap_servers=[config.CONNECTION['host'] + ':' + config.CONNECTION['port']],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='articles_consumer',
    value_deserializer=lambda x: loads(x.decode(constants.UTF_ENCODING)))


def format_message(message):
    message['title'] = ' '.join(message['title'])
    message['text'] = ' '.join(message['text'])
    return message


def main():
    print('Started ' + ARTICLES_TOPIC + ' consumer')
    for message in unfiltered_consumer:
        message = format_message(dict(message.value))
        url = message['url']
        print('new message')

        existing_article = articles_service.find_article(url)
        if existing_article is None:
            similar_articles = articles_service.find_similar_articles(message['text'], MIN_SIMILARITY_SCORE)
            if not similar_articles:
                articles_service.insert_article(message)
            else:
                print('message: ' + str(message))
                print(similar_articles)
        else:
            articles_service.delete_article(url)
            articles_service.insert_article(message)


if __name__ == "__main__":
    main()
