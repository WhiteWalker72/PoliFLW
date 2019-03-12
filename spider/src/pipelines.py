results = []


class ResultPipeline(object):
    """ A custom pipeline that stores scrape results in 'results'"""

    def process_item(self, item, spider):
        results.append(dict(item))
