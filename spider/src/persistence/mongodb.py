import pymongo
import urllib

client = pymongo.MongoClient("mongodb+srv://admin:" + urllib.parse.quote("poliflw9@") + "@poliflw-p58zy.mongodb.net/test?retryWrites=true")
db = client["spider_service"]
sources_collection = db["sources"]

sources_collection.create_index([('text', 'text'), ('title', 'text')])
