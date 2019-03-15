from kafka import KafkaProducer
import src.config as config
import src.constants as constants
from json import dumps


class Producer:
    def __init__(self, topic):
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=[config.CONNECTION['host'] + ":" + config.CONNECTION['port']],
                                      value_serializer=lambda x:
                                      dumps(x).encode(constants.UTF_ENCODING)
                                      )

    def send_message(self, message):
        self.producer.send(self.topic, value=message)
