from src.persistence.mongodb import sources_collection as collection
import math


def find_sources():
    return list(collection.find())


def get_websites():
    sources = find_sources()
    urls = [x['website'] for x in sources]
    return list(filter(lambda x: type(x) is str or not math.isnan(x), urls))


def add_source(source):
    collection.insert_one(source)


def find_source(url):
    return collection.find_one({'url': url})


def delete_source(url):
    return collection.delete_one({'url': url})



