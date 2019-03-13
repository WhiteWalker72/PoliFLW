from src.producer import Producer

results = []
producer = Producer('unfiltered-articles-input')


class ResultPipeline(object):
    """ A custom pipeline that stores scrape results in 'results'"""

    @staticmethod
    def process_item(item, spider):
        # producer.send_message(dict(item))
        results.append(dict(item))
