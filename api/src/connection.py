import pymongo
import urllib

client = pymongo.MongoClient("mongodb+srv://admin:" + urllib.parse.quote("poliflw9@") + "@poliflw-p58zy.mongodb.net/test?retryWrites=true")
db = client["api_service"]
sources_collection = db["sources"]


def get_client():
    return client


def get_all_sources():
    return sources_collection.find()


def insert(new_source):
    db.sourcesCol.insert(new_source)
    return True
