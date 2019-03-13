import pymongo
import urllib

client = pymongo.MongoClient("mongodb+srv://admin:" + urllib.parse.quote("poliflw9@") + "@poliflw-p58zy.mongodb.net/test?retryWrites=true")
poliflwDB = client["poliflw"]
sourcesCol = poliflwDB["sourcesCol"]


def get_client():
    return client


def get_all_sources():
    return sourcesCol.find()


def insert(newSource):
    poliflwDB.sourcesCol.insert(newSource)
    return True